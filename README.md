# MUXI
![logo](https://avatars2.githubusercontent.com/u/10476331?v=3&s=200)

> a Decorated Python Web FrameWork
>    for study not product

## Hello From Muxi
***index.py***

    from muxi import Muxi
    from muxi.de import url, views, headers, config

    @config(secret_key='xxx')
    def create_app():
        app = Muxi(__name__)
        return app

    app = create_app()

    @url(app, '/index')
    @views('index.html')
    @headers(status_code=200)
    def index():
        return {'name': 'muxi'}

***index.html***

    <html>
        <body>
            <h1>Hello {{ name }}</h1>
        </body>
    </html>

## More Features

+ **Database Connection Decorator**
+ **Wtforms**
+ **Sqlalchemy**

## About Name
muxi is my team name MuxiStudio(木犀团队)<br/>
[MuxiStudio](https://github.com/Muxi-Studio)

## LICENSE

    (The WTFPL)

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

    Copyright (C) 2016 neo1218 (https://github.com/neo1218)

    Everyone is permitted to copy and distribute verbatim or modified
    copies of this license document, and changing it is allowed as long
    as the name is changed.

               DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
      TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

     0. You just DO WHAT THE FUCK YOU WANT TO.

