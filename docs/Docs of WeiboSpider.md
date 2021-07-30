# Docs of WeiboSpider

本项目是基于开源爬虫框架Scrapy进行开发的，因此在对本项目的配置文件等进行修改时，请仔细阅读[Scrapy](https://docs.scrapy.org/en/2.4/ )官方文档，避免出现奇奇怪怪的错误。

本项目的代码组织结构如下所示。其中`scrapy.cfg`是Scrapy爬虫的配置文件，由Scrapy自动生成，一般情况下不对其进行修改；`init`目下保存了爬虫运行依赖环境初始化脚本；`WeiboSpider`目录下则是爬虫的代码。

````
.
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

在`init`目录下保存了创建保存爬虫数据的MongoDB Container创建脚本`init/init.sh`、环境清理脚本`init/clean.sh`和MongoDB初始化 Javascript脚本`init/resource/db_init.js`三个文件。

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

在完成了MongoDB Container的创建之后，需要执行命令`sudo docker exec -it weibo mongo 127.0.0.1:27017 /etc/resource/db_init.js`运行MongoDB初始化脚本。

`Db_init.js`脚本首先会创建两个分别名为`admin`和`weibo`的数据库。对于`admin`数据库，`db_init.js`会创建名为`admin`的管理员用户，其权限为`root`；同理对于`weibo`数据库该脚本会创建名为`weibo`的普通用户，爬虫所有爬取到的数据都会保存在`weibo`数据库中，`weibo`用户的权限为`readWrite`.

最后，`db_init.js`脚本会创建`user`、`tweet`等集合，具体信息如下表。

| Collection  | 数据类型      |
| ----------- | ------------- |
| `user`      | 用户账户资料  |
| `tweet`     | 用户博文      |
| `longtext`  | 用户长文本    |
| `error_log` | 爬取失败的URL |

### WeiboSpider

`WeiboSpider`目录结果如下所示，该目录下包含了



#### Base

#### Conofig

#### Spiders

#### Items

#### Pipelines

#### Middlewares

### Database

### Extension

#### 我需要做什么？

#### 定义你自己的爬虫