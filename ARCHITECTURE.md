## Общая архитектура приложения

Само приложение крайне мало, поэтому показалось уместнее и удобнее 
описать его работу в одном файле, помимо doc добавлений.

-----

Все начинается в [app_server.py](server/app_server.py) 
Вы можете видеть, что там стартуется простенький HTTP server, который и будет обрабатывать запросы

`server = ThreadingHTTPServer(('', int(CONFIG.port_number)), RequestHandler)`

у которого обработчиком api requests будет [RequestHandler](server/app_server.py)

потом также инициализируется [Mp3Storage](server/utils/mp3_storage.py).

По факту это два (**RequestHandler**, **Mp3Storage**) основных компонента, 
которые необходимо разобрать. 

----
#### [Mp3Storage](server/utils/mp3_storage.py)

[Mp3Storage](server/utils/mp3_storage.py) - сохраненная в dict коллекция файлов mp3 в работе.


Где файлы представлены ввиде  `route_id$$hash$$created_time.mp3`. То есть маппинг организован так, 
`route_id -> StorageValue`. 

[StorageValue](server/utils/mp3_storage.py) - сущность хранящая путь к файлу, хэш контента, 
время работы с ним и future таску, которая за это отвечает. 

Имея три последних поля можно понять, что под route_id лежит именно нужный контент (по хэшу), 
что файл не был кем-то переписан в обход нашего [Mp3Storage](server/utils/mp3_storage.py) 
и как-то влиять на работу с этим контентом через future.

Самый сложный метод для осознания и лучший для понимания может быть `get_or_create_value()`, 
так как остальные методы не сильно отличаются от тех же в классе dict.

 
Метод `get_or_create_value()` руководствуется следующей логикой, если элемента нет, то он его создает, если он до этого был, то проверяет, что он был 
не закорапчен и то, что по предыдущему route_id спросили именно такой текст, сравнивая по хэшу. Если что-то пошло не 
так, то пытается остановить предыдущию работу с этим файлом и пересоздать новый элемент. 

_Пример, когда что-то могло пойти не так:_

Пользователь перепослал тот же route_id дважды но второй раз уже с другим контентом, тогда отменяем предыдущию 
работу и начинаем заново с новым контентом. Под отменой работы понимается удаление таски ассоциированной с элементом из 
очереди, так как выходит по ней уже другой контент, а затем создание новой таски с правильным контентом.


----
#### [RequestHandler](server/app_server.py)

Задача этого handler делегировать другим handlers. И он краине просто и customizable, так как по факту позволяет 
производить чуть ли не полную настройку под себя, в отличие от современных frameworks. 

На момент написания этой заметки было их 4 штуки

`NotActivatedStorageHandler` - пишет что еще [Mp3Storage](server/utils/mp3_storage.py) не просканировал папку с файлами.

`WelcomePageHandler` - создает вступительную страницу с первоначальной статистикой о [Mp3Storage](server/utils/mp3_storage.py)

`FileDownloadHandler` - просто пишет блоки байтов файла в конекцию 

`ApiHandler` - производит работу с endpoints описанными в README.md

Все handlers крайне просты, может быть кроме `ApiHandler`, так как там есть немного логики, давайте на его примере попытаемся
расширить функциональность сервиса. И вместе с этим файлом комментариев прилетит коммит с этой 
расшириной функциональностью. 

Пусть я хочу обрабатывать не только json вариант, но и `string -> audio`, посмотрим, что мы должны поменять

заходим в [ApiHandler](server/controllers/handle_api_request.py) и видим что есть mapping urls на обработчики, названный 
`ROUTES`, давайте наш назовем `string_to_audio` и добавим в список. После этого нам необходимо написать сам обработчик, для этого
заходим в [api_methods](server/controllers/api_methods.py) и добавляем свой StringToAudio (это все).
 
```python
class StringToAudio(ApiMethod):
    def __call__(self, handler: BaseHTTPRequestHandler, json_data):
        # check request
        error_msg = check_json_data(json_data, [FIELD_ROUTE_ID, FIELD_ROUTE_TEXT])
        if error_msg:
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        text = f"<p>{json_data[FIELD_ROUTE_TEXT]}</p>"
        route_id = json_data[FIELD_ROUTE_ID]
        log(f"For Route ID : {route_id} got {text}")

        if not text:
            error_msg = f"No text provided"
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        if len(text) > CONFIG.text_length_limit:
            error_msg = f"Too large text (> {CONFIG.text_length_limit} characters)"
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        text_hash = hash_text(text)
        (is_created, value) = MP3_STORAGE.get_or_create_value(route_id, text_hash)

        # check for repeated requests
        if not is_created:
            if value.is_done():
                return prepare_api_response(handler, HTTP_OK, "ALREADY_DONE")
            elif value.is_processed():
                return prepare_api_response(handler, HTTP_CREATED, "ALREADY_HAVE_TASK")

        value.future = executor.submit(
            executor.route_to_audio_task, executor.route_to_audio_callback, value, route_id, text, text_hash
        )

        return prepare_api_response(handler, HTTP_OK, "OK")`
 ```
 
 
теперь делая запрос вида:
```json
{
  "route_id": "123235",
  "route_text": "haha"
}
```

будет выдаваться файл по id.

-----

Мы можем сделать, как в framework-ах по декоратору. А давайте собственно добавим это и сюда. 
Напишем свой маленький декоратор, а потом создадим endpoint, который будет говорить, что сервис еще не выключен.


декоратор
```python
def request_mapping(request_url: str = ""):
    if request_url == "":
        raise ValueError("Provide request url!")
    if request_url in ROUTES:
        raise ValueError("Request url is already taken!")

    def dec(func):
        if func is None:
            raise ValueError("callback is None!")
        method = functools.wraps(func)(ApiMethod())
        method._to_replace = func
        ROUTES[request_url] = method

    return dec
```

endpoint

```python
@request_mapping("/heart_beat")
def heart_beat(handler: BaseHTTPRequestHandler, json_data):
    return prepare_api_response(handler, 200, "heart_beat")
```

теперь сервис выдает heart_beat по запросу. 





 

