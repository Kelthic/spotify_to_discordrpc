## Проигрываемый трек из Spotify в Discord RPC

**Скрипт выводит в Discord Активность**:
* Исполнителя;
* Название трека;
* Обложку трека;
* Текущее время проигрывания.

**Также, скрипт выводит информацию в консоль**:
* Исполнителя;
* Название музыкального трека.

**Создаётся лог и его бэкапы в котором**:
* Время вывода трека;
* Исполнитель(-и) и лейбл;
* Ошибки (для отладки).

## Что это?

Это скрипт, который позволяет выводить в свою активность треки из Spotify.
К несчастью, Discord перестал выводить проигрываемые треки из Spotify в активность пользователей из России и Беларуси. В связи с этим было принято решение написать скрипт, потому что мириться с этим желания нет.

## Установка

* Скачайте мой репозиторий;
* Создайте [приложение](https://developer.spotify.com/) в среде разработки Spotify;
    * В Redirect URL укажите http://localhost:8888/callback
    * Сохраните **cliend_id** и **client_secret** в любое удобное вам место
* Создайте [приложение](https://discord.com/developers/) в среде разработки Discord;
    * Сохраните app_id от вашего приложения
    * Имя можете дать любое, но предпочитетьнее "Сейчас играет" или "Now playing" для эстетичности
* Откройте файл **config.ini** и вставьте **client_id**, **client_secret** и **app_id** в соответствующие строки;
* Запустите start.bat и наслаждайтесь
    * Можете запускать main.py через командную строку в директории, если вас не устраивает .bat файл.
## Как это выглядит в Discord?
![Демонстрация активности в Discord](https://i.postimg.cc/k5XdG0wh/image.png "Демонстрация активности в Discord")

