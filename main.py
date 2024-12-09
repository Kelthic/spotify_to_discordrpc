import time
import logging
import configparser
from pypresence import Presence
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import shutil

# Функция для создания бэкапа лог-файла
def backup_log_file(log_filename):
    if os.path.exists(log_filename):
        # Проверим, существует ли уже бэкап
        for i in range(1, 10):
            backup_filename = f"{log_filename}.backup_{i}"
            if not os.path.exists(backup_filename):
                shutil.copy(log_filename, backup_filename)  # Копируем лог в бэкап
                print(f"Бэкап создан: {backup_filename}")
                return
        # Если все бэкапы с цифрами 1-9 существуют, перезапишем последний
        shutil.copy(log_filename, f"{log_filename}.backup_9")
        print("Все бэкапы существуют, последний перезаписан.")

# Функция для очистки и создания бэкапа лог-файла
def reset_log(log_filename):
    if os.path.exists(log_filename):
        backup_log_file(log_filename)  # Создаем бэкап перед очисткой
        with open(log_filename, 'w'):
            pass  # Очистить файл

# Создаём папку для логов, если её нет
log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Путь к лог-файлу и бэкапам в папке ./logs
log_filename = os.path.join(log_dir, "spotify_discord.log")

# Настройки логирования
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Загрузка конфигурации из config.ini
config = configparser.ConfigParser()
config.read("config.ini")

SPOTIFY_CLIENT_ID = config.get("Spotify", "client_id")
SPOTIFY_CLIENT_SECRET = config.get("Spotify", "client_secret")
SPOTIFY_REDIRECT_URI = config.get("Spotify", "redirect_uri")
SPOTIFY_SCOPE = config.get("Spotify", "scope")
DISCORD_CLIENT_ID = config.get("Discord", "client_id")

# Настройки Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
))

# Настройки Discord
rpc = Presence(DISCORD_CLIENT_ID)
rpc.connect()

# Максимальный размер лог-файла (1 МБ)
MAX_LOG_SIZE = 1 * 1024 * 1024  # 1 Мегабайт

def get_album_cover_url(track):
    """Получает URL обложки альбома."""
    images = track['album']['images']
    if images:
        return images[0]['url']  # Самое большое изображение
    return None

def update_discord_presence(track, playback):
    """Обновляет активность Discord."""
    progress = playback['progress_ms'] // 1000
    duration = track['duration_ms'] // 1000
    track_name = track['name']
    artist_name = ', '.join(artist['name'] for artist in track['artists'])
    cover_url = get_album_cover_url(track)

    # Ссылки
    track_url = track['external_urls']['spotify']  # Ссылка на трек
    github_url = "https://github.com/kelthic"  # Пример ссылки на GitHub

    # Вычисляем окончание трека
    end_time = time.time() + (duration - progress)

    # Обновление активности
    rpc.update(
        state=f"📜Title: {track_name}",
        details=f"🗣Artist: {artist_name}",
        buttons=[  # Здесь передаем кнопки в формате JSON
            {"label": "🎧 Listen in Spotify", "url": track_url},
            {"label": "🌐 Author", "url": github_url}
        ],
        large_image=cover_url,
        large_text=f"{artist_name} - {track_name}",
        start=time.time() - progress,
        end=end_time
    )
    logger.info(f"Записанный трек: {artist_name} - {track_name}")
    print(f"Обновлено: {artist_name} - {track_name}")

# Основной цикл
last_track_id = None
try:
    reset_log(log_filename)  # Очистка и создание бэкапа при запуске программы

    while True:
        try:
            playback = sp.current_playback()
            if playback and playback['is_playing']:
                current_track = playback['item']
                current_track_id = current_track['id']

                if current_track_id != last_track_id:  # Проверяем смену трека
                    update_discord_presence(current_track, playback)
                    last_track_id = current_track_id
            else:
                rpc.clear()
                last_track_id = None
                logger.info("Ничего не играет")
                print("Ничего не играет")
        except Exception as e:
            logger.error(f"Ошибка: {e}", exc_info=True)

        # Проверяем размер лог-файла и очищаем, если он стал слишком большим
        if os.path.exists(log_filename) and os.path.getsize(log_filename) > MAX_LOG_SIZE:
            reset_log(log_filename)

        time.sleep(2)  # Проверяем каждые 2 секунды
except KeyboardInterrupt:
    logger.info("Программа остановлена пользователем")
    print("Остановлено.")
