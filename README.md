Проект в вocker [контейнере](https://hub.docker.com/r/nexus07/book_store_deep_longeviry)
запускать:
`git clone git@github.com:nexus-07/book_store_deep_longevity.git`
`docker pull nexus07/book_store_deep_longeviry:latest`
`docker-compose run --rm web`

Логин и пароль в админку
admin / admin
Токен для доступа по API (так же он выводится в момент первого запуска контейнера):
`Token f4f9b4af1f8357d21e27db19af3fa497cd0ac9a7`

исходники на gitlab:
`https://github.com/nexus-07/book_store_deep_longevity`

_Разработка приложения задержалась потому, что ранее небыло опыта работы с docker и c DRF, пришлось их глянуть с нуля._ 
_Основное время занаяло именно подготовка и развертывание проекта, настройка._

_Добавлена модель `BookChapter`(она не используется), что бы показать дальнеейшее расширение функционала, и почему таблицы разделены на более мелкие сущности._