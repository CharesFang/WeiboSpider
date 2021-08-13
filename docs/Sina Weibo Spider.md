# Sina Weibo Spider

本项目是基于开源爬虫框架Scrapy进行开发的，因此在对本项目的配置文件等进行修改时，请仔细阅读[Scrapy](https://docs.scrapy.org/en/2.4/ )官方文档，避免出现奇奇怪怪的错误。

本项目的代码组织结构如下所示。其中`scrapy.cfg`是Scrapy爬虫的配置文件，由Scrapy自动生成，一般情况下不对其进行修改；`init`目下包含了创建爬虫运行环境的初始化脚本`init.sh`以及相关资源文件等；而`WeiboSpider`目录下是爬虫的实现代码。

````
├── LICENSE
├── Readme.md
├── WeiboSpider
├── docs
├── img
├── init
├── requirements.txt
└── scrapy.cfg
````

### Init

在`init`目录下保存了创建保存爬虫数据的MongoDB Container创建脚本`init/init.sh`、清理脚本`init/clean.sh`和MongoDB初始化 Javascript脚本`init/resource/db_init.js`三个文件。

#### Init.sh

`Init.sh`脚本会在当前用户的根目录`$HOME`下创建`mongo`根目录以及`data`、`config`等子目录，用于持久化存储MongoDB Container数据,然后`init.sh`会创建Docker Container并做相应的目录映射。`init.sh`创建的目录及对应作用如下表所示。

| 路径                   | 说明                                                         |
| :--------------------- | :----------------------------------------------------------- |
| `$HOME/mongo`          | MongoDB Container数据存储根目录，MongoDB所有的配置文件、日子和运行数据等都保存在此根目录下。 |
| `$HOME/mongo/data`     | 存储MongoDB数据。                                            |
| `$HOME/mongo/config`   | 存储MongoDB配置文件`mongo.conf`.                             |
| `$HOME/mongo/log`      | 存储MongoDB运行日志`mongo.log`.                              |
| `$HOME/mongo/resource` | 存储MongoDB初始化 Javascript脚本`db_init.js`并将其映射到MongoDB Container的`/etc/resource`目录下。 |

最终，`init.sh`脚本创建了名为`weibo`的MongoDB Container，可以通过命令`sudo docker ps -a`查看容器详情。

#### Db_init.js

在完成了MongoDB Container的创建之后，需要执行命令`sudo docker exec -it weibo mongo 127.0.0.1:27017 /etc/resource/db_init.js`运行MongoDB初始化脚本，其根据MongoDB提供的API接口实现。

`Db_init.js`脚本首先会创建两个分别名为`admin`和`weibo`的数据库，其中`admin`数据库用于存储MongoDB数据库管理用户信息，`weibo`数据库存储爬虫采集到的数据。对于`admin`数据库，`db_init.js`会创建名为`admin`的管理员用户，其权限为`root`；同样的，对于`weibo`数据库该脚本会创建名为`weibo`的普通用户，爬虫爬取到的所有数据都会保存在`weibo`数据库中，`weibo`用户的权限为`readWrite`.

最后，`db_init.js`脚本会创建`user`、`tweet`等集合，每个集合存储的具体用户数据类型如下表所示。

| Collection  | 数据类型      |
| ----------- | ------------- |
| `user`      | 用户账户资料  |
| `tweet`     | 用户博文      |
| `longtext`  | 用户长文本    |
| `error_log` | 爬取失败的URL |

### WeiboSpider

`WeiboSpider`包含了微博爬虫的数据采集、清洗和存储等功能的实现以及爬虫相关配置文件等，其结构如下所示。

```
├── __init__.py
├── base
├── config
├── database
├── items
├── middlewares
├── pipelines
├── resource
├── settings.py
└── spiders
```

#### Base

`Base`目录下定义了WeiboSpider的三个抽象类，分别为`BaseSpider`、`Config`和`Pipeline`，为爬虫的扩展和实现进行了规范。

##### BaseSpider

`BaseSpider`是一个抽象类，其继承了`	scrapy.Spider`，并要求用户在调用任意爬虫时，必须传入`uid`参数以指定目标爬取对象，其中`uid`参数是指以`|`符号为分割的新浪微博用户uid字符串，其形如`123456|654321`。

同时，`BaseSpider`还实现了`get_uid_list`方法，对用户输入的`uid`字符串分割、转换并以`list`存储uid。

最后，`BaseSpider`同样实现了`parse_err`方法，该方法会在`IgnoreRequest`（关于`IgnoreRequest`详见Scrapy文档[IgnoreRequest](https://docs.scrapy.org/en/2.4/topics/exceptions.html?highlight=ignoreRequest#ignorerequest)） 被Scrapy捕获时执行，然后生成保存爬取失败的`Request`对象相关信息的`ErrorItem`，最终存储到MongoDB数据库的`error_log`集合中。

##### Config

`Config`也是一个抽象类，定义了`gen_url`抽象方法，用于根据不同类型的爬取目标和目标用户生成目标URL，获取微博用户数据。

继承`Config`的子类通常会根据不同类型的微博数据，写入数据获取API，并实现`gen_url`，返回目标URL。其子类的具体实现，见后文[Config](#config)章节。

##### Pipeline

`Pipeline`同样也是一个抽象类，用于规范爬虫中存储数据的各类管道的实现。`Pipeline`在被实例化时，能够通过`DBConnector`类创建MongoDB数据库连接。

`Pipeline`首先实现了`open_spider`与`close_spider`两个方法，分别用于创建和关闭MongoDB数据库连接。这两个方法会在爬虫被开启或关闭时分别被调用。（*"This method is called when the spider is opened/closed"*）关于上述两个方法详见Scrapy文档 [Item Pipeline]("https://docs.scrapy.org/en/2.4/topics/item-pipeline.html").

`Pipeline`还定义了一个名为`process_item`的抽象方法，所有继承的`Pipeline`的子类都必须实现该方法以实现对不同类型的爬取对象的处理。

#### Conofig

<span id="Config"></span>

#### Spiders

#### Items

#### Pipelines

#### Middlewares

#### Database

### Extension

#### 我需要做什么？

#### 定义你自己的爬虫