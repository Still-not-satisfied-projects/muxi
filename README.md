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

## 备注
这个框架只是一个玩具式的框架,
是为了更好的学习Python后端框架的知识,为了[这篇博客](http://neo1218.github.io/framework/)编写的。
<hr/>
但是这个框架仍然融合了我的一些思想: 比如装饰器的大量使用...(装饰器大法好)...
<hr/>
我来谈谈我的框架设计吧:<br/>

1. **装饰器**<br/>
这个其实没有什么设计, 仅仅是因为我喜欢装饰器, 喜欢这种简单的模式,
而且我想看看大量使用装饰器导致的头重脚轻的代码😄a<br/>
2. **create app**<br/>
因为我的框架没有蓝图, 使用create_app的话方便创建多个app,
当然app之间的交互是一个大问题...<br/>
3. **db 模块**<br/>
ORM用多了是有毒的, 所以多用用db吧, 直接写sql语句, sql大法好!!!!<br/>
4. **表单系统**<br/>
没有表单系统哈哈哈哈!!!直接前端写表单, 后端通过request获取就可以了!<br/>
5. **前端模版**<br/>
前端模版打算自己写, 因为这个比较有意思的柑橘<br/>


