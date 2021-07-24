# Sina Weibo Spider

![](https://img.shields.io/badge/License-GPL-brightgreen) ![](https://img.shields.io/badge/Scrapy-v2.4-blue) ![](https://img.shields.io/badge/Python-v3.8-orange) ![](https://img.shields.io/badge/Spider-Weibo-yellow)

## Preface

这个微博爬虫的实现近乎贯穿了我本科学习大半的时间。前前后后经过了大约有3次颠覆级别的重构之后，现在看起来也算是稍微有了那么一点点看得过去的样子。经过小半个月的摸鱼划水，我也完成了对这个微博爬虫从架构的重构到具体实现的优化，以及设计提供自动化部署脚本等工作，使得这个爬虫比较与v1.0版本简直是高到不知道哪里去了（膜法警告:
warning:）。

总而言之，在不断对地对代码进行重构和优化的过程中，我也在不断地学习。前路漫长，要学的东西还有很多，如果可能的话我会长期对这个项目进行维护（前提是有空摸鱼），也会提供尽可能详细的说明文档，欢迎各位大手子提PR或者Issue，同时也求一个小小的star，也算是我为诸位还在为如何从微博采集数据烦恼的研究者们做出的一点微小的贡献吧。

## 为什么选择M站采集数据？

首先要说明最重要的一点是，本项目是基于开源爬虫框架**[Scrapy](https://scrapy.org/)**，针对新浪微博的**移动站点**，即**M站**（https://m.weibo.cn/），实现的一个**单机**、**高并发**的轻量微博爬虫。解释一下什么是新浪微博的M站。随着一堆乱七八糟的技术的迅速发展（别问，问我我也不懂是啥），越来越多的国产手机APP（此处特指安卓下）都倾向于在APP内置一个游览器内核（一般来说都是chromium，不过可能伴随一些魔改），然后通过前端开发实现APP的快速迭代。M站简单明了的说，就是用于为手机客户端的微博APP提供数据来源。（这一段中包含了我许许多多的胡说八道，如果有各种离谱的错误请尽管喷我）

通常，在实现爬虫之前，开发者都需要对目标站点的反爬措施进行充分的调研，然后才下手开干。对于微博来说，现目前已知有三个不同的域名都能够使用其提供的服务，分别是PC站（https://weibo.com/），M站（https://m.weibo.cn/）和一个我不知道该怎么称呼并且十分简陋的站（https://weibo.cn/）。所谓PC站就是使用PC端游览器访问新浪微博所看到的网站，M站即前文所述，十分简陋站我现在也不知道是干嘛的，就很尴尬。

这三个站在反爬措施的严格程度上差异较大，其中PC站的反爬措施是最严格的，而M站和十分简陋站的反爬措施设置较为宽松。这之中的道理也很简单，PC站一般而言作为诸多爬虫爱好者的首选目标，自然是承受了非常多的爬虫流量，新浪微博当然也会部署最为严格的反爬措施保证他不会被乱七八糟的爬虫搞崩掉。据我不那么完全的观察，github上现存有数个在2-3年前就已经停止维护的针对PC站的微博爬虫。大概总结一下他们为了绕过PC的反爬措施需要做的工作：

1. 首先是购买一批专门用来爬数据的小号，构建一个账户池。
2. 仔细分析研究新浪微博的认证机制， 实现自动化的模拟登录，期间可能还会遇到验证码识别等困难。
3. 通过模拟登录之后的账户，构建cookie池，用这些cookie进行下一步的爬取。
4. 购买一定数量的代理IP，为每个cookie绑定代理IP。
5. 经过冲冲磨难最终才绕过了反爬，在爬取的过程中还要注意各cookie-IP的负载均衡，在cookie失效之后需要即使的清理。
6. 综上所述，针对PC站爬取数据属实头铁，就算拿到数据之后还需要复杂的数据清洗，才能够得到最终的用户数据，并且采集效率极低，出错率高。

与之相反的是，微博的M站和十分简陋站的反爬措施就宽松很多。针对十分简陋站，有大佬已经开发了十分完整且可用性极强的爬虫（此处放上传送门[nghuyong:WeiboSpider](https://github.com/nghuyong/WeiboSpider)），能够获取千万级别甚至更高数量级的数据，能够采集到较为完整的微博用户数据。但这个爬虫有一个问题在于，即使十分简陋站的反爬较为宽松，但**仍然需要购买小号建立cookie池**之后才可以进行数据采集。当然，为了提高数据采集的速率，代理IP也是需要的。

综上所述，偷鸡的我选择了微博的**M站**开发爬虫，无需买小号构建cookie池，甚至也不需要代理IP（对采集速度有很大的限制），就实现了一个轻量高效地微博爬虫。

## 设计原理

简单阐述一下M站微博爬虫的设计原理。打开Firefox游览器（Chrome，Safari啥的都行），输入任意一个微博用户主页的网址，这里随便拿一个公众明星的账户举例（https://m.weibo.cn/u/3669102477）。通过F12开发者工具，观察微博M站数据加载的过程，如下图所示。重点观察红框内的两个请求。事实上微博的M站通过**AJAX**来异步加载用户数据，红框内对应的两个链接，实际为鞠婧祎这个用户的账户信息获取接口，将它提取出来即为：

`https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1005053669102477`

显然，`3669102477`是鞠婧祎这个账户的**UID**，而`containerid`的构造方法为`10050+uid`，由此分析得出了M站中用户账户资料的数据获取接口。

<img src="img\1.png" style="zoom:50%;" />

打开刚刚分析得到的数据接口，获取到JSON格式的用户数据，如下图所示，可以直接存储到MongoDB等非关系型数据库中。

<img src="img\2.png" style="zoom:50%;" />

同理可推，只要针对微博M站进行仔细的人工分析，提取出用户数据获取接口是能够实现的。并且，通过这样的数据接口获取数据不需要进行**用户认证**
，意味着即使没有用户Cookie，也能够对新浪微博进行大规模的数据采集，本项目也是基于这样的原理进行构建。

## 为什么使用针对M站的微博爬虫？

咳咳，虽然不免有王婆卖瓜的嫌疑，但也要对本项目的有点进行一下简要的阐述。

1. 轻量：本项目的核心代码大概在500行左右，由于选择了最轻松的道路，所以实现的过程十分愉快，也尽可能的维持了本项目的可扩展性和易用性，加之提供了一键部署脚本，保证在使用上能够做到轻松愉悦。
2. 易用：本项目不需要构建额外的用户池，最多只需要使用额外的代理IP来提高采集速度，就可以实现10万级别的用户数据采集，易用性非常高。
3. 迅速：由于爬取到的数据本身即为json格式，所以基本无需进行数据清洗，也大大提高了爬虫的采集速率。

## To Start

### 运行环境

- Python >= 3.6.0，开发环境的Python版本为3.8.10
- MongoDB >= 4.2
- 操作系统常见的Linux发行版

### 初始化

### 数据采集

## Docs

### Init

### WeiboSpider

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

## 初步完成代码重构！

通过这小半个月以来的摸鱼划水，初步完成了爬虫代码的重构，完成了基本对微博用户资料、博文的爬取，重构了代码结构（虽然某种程度上还是很ugly）

总结一下现目前完成的工作和还需要进行的工作：

1. 对爬虫架构进行重构，增强了可扩展性和可维护性。

2. 新增`init/init.sh`MongoDB自动化部署脚本（需要docker支持）

3. 完成了`user_info_spider`和`tweet_spider`，可以使用如下命令调用爬虫

   `scrapy crawl user_info_spider -a uid=xxxx|xxxx`

   `scrapy crawl tweet_spider -a uid=xxxx|xxxxx`

4. 提供了四大下载中间件，可以根据需求自行开启或关闭。

   1. `RetryMiddleware`
   2. `FakeUserAgentMidlleware`
   3. `InitialMiddleware`
   4. `ProxyMidlleware`

未完成的工作：

1. 实现对`user_info_spider`和`tweet_spider `的封装。
2. 对热搜、用户粉丝关注列表等信息的爬虫。
3. 看得懂的Readme（对不起我太懒了--）
4. 更易读的技术文档（现目前这玩意儿就没有）

## Warning!

终于放假并且摆脱了老板的魔爪，并且能够捡起自己去年这个时候写下的屎山代码~~（不是）~~

给自己定下了几个小目标，争取九月份之前，完成对爬虫的重构，实现代理池、中间件等模块化设计，并或许可能应该支持docker一键部署爬虫+数据库。旧的代码存储在了`v1.0`分支中，暂时还是可以使用的，新版微博爬虫在`dev`
分支中进行开发，这里要特别感谢对我爬虫提出意见和改进的cyc大佬，当然由于特殊的原因我暂时无法联系他，也没办法将他加入到contributor中。

综上，开搞开搞。

## 以下是原版正文

这是一个基于 **Scrapy** 框架的迷你新浪微博爬虫，无需维护Cookie或者进行模拟登录，可以实现对新浪微博的较大规模数据采集。

大概是在19年的九月份，那时我还很菜（当然现在也很菜），由于项目需要被逼上马，前前后后折腾了大概一两个月，写出了这个爬虫的第一版。当然，现在回顾大约一年前自己写的代码，果然是不堪回首，难以入目，不管是从代码的简洁性、可读性还是可维护性看起来都是一坨shit。20年初参加了某个全国性的比赛，借机重构了这个爬虫，比起第一代的爬虫而言，砍掉了那些实在过于冗余的代码，调整了项目的结构，现在看起来总算是清爽很多了。

言归正传，**Tiny Weibo Spider** 是我基于新浪微博的移动站点（m站）[m.weibo.cn](https://m.weibo.cn/) 和 **Scrapy** 框架构建的一个轻量微博爬虫，并将采集到的数据存储到 **MongoDB** 中包括Scrapy框架初始化时自动创建的代码，加上一对乱七八糟的注释和缩进换行，总共的代码量也只有1500行左右，其中核心代码我估计也就300行上下。核心代码量虽然不多，但是实现的功能依然较为齐全。与针对微博PC站也是就 [weibo.com](https://weibo.com/) 使用者不需要去购买小号来进行模拟登录，然后抓取Cookie，维护一个用户池，单纯的使用单个IP也可以对微博中的用户数据进行采集；如果要进行大规模的数据采集，只需要使用代理IP即可（欢迎各大代理商找我投放广告）。

现目前这个微博爬虫只能部署在单个主机上运行，后面也可以开一个分支拓展成分布式的，不过最近升学压力有点大，可能要无限鸽了。据不准确估计，在有充足的代理IP的情况下，每天抓取的用户信息数量至少也是在**百万**及以上，顺带抓取了**千万条**博文，对于大部分的数据挖掘和分析工作来讲，我觉得这个采集效率是完全足够了？

### 项目说明

这是一个基于 **Scrapy** 框架的新浪微博爬虫，爬取的主要目标是新浪微博m站的数据，同时并使用了MongoDB对于爬取到的用户数据进行存储。

#### 为什么选择M站爬取数据

新浪微博的m站，即 [m.weibo.cn](https://m.weibo.cn/) ，为新浪微博的手机、平板等移动客户端提供数据。其中，绝大部分用户数据是以 **Ajax** 的形式**异步**请求加载的。由于新浪微博的PC站对于第三方爬虫部署了严格的反爬措施，包括必须要求用户登录才能够获取完整数据，暂时封禁某个请求过于频繁的IP地址等等，而新浪微博的M站的反爬措施相比PC站较少，用户不需要登录就可以获取足够完整的数据信息，因此，本项目选择新浪微博的m站进行爬取。但新浪微博m站中的用户数据分布较为零散，在获取同样完整性的数据前提下，面向m站的微博爬虫需要发起更多的网络请求，这也是限制这个爬虫爬取效率的一个原因。

#### 实现原理

前文中提到，新浪微博的m站以 **Ajax** 的形式异步请求用户数据，只要能够找到微博加载用户数据的URL，提取API接口，能够实现快速爬取微博用户数据。不得不说这是一种很取巧的爬取策略，新浪微博并没有针对这些 Ajax 数据请求接口进行身份认证（貌似现实中要认证也不太可行？），来自任意IP的正确请求都能够获得返回的数据，从而避免了模拟登录，用户池维护一堆麻烦的事情，某种程度上来说也算是提升了爬取效率。

以下图这个用户为例，首先通过微博m站访问用户的[主页](https://m.weibo.cn/u/5653796775)，然后打开F12开发者工具，查看m站发起的Ajax请求。

<img src="img\1.png" style="zoom:50%;" />

如下图所示，可以看到几个被触发的Ajax请求响应状态和信息，选择返回大小最大的包进行查看。

<img src="img/2.png" style="zoom:67%;" />

如下图所示，可以观察到微博服务器返回了json的形式用户数据。**即针对特定用户构造特定的数据请求URL，就能够实现用户数据地有效爬取**。这一点是这个本项目爬虫构建的关键。

<img src="img/3.png" style="zoom:50%;" />



#### 功能说明

本项目现目前总共实现了四个爬虫，其主要功能如下表所示。

| 爬虫名称        | 功能                                   |
| :-------------- | :------------------------------------- |
| WeiboSpdier     | 爬取指定用账户与博文信息               |
| FansListSpider  | 爬取指定用户粉丝与关注列表用户信息     |
| HotSearchSpider | 爬取现目前实时热搜                     |
| KeyWordsSpider  | 根据用户指定的关键词爬取用户发布的博文 |

### 运行环境

- Python >= 3.7.0
- MongoDB >= 3.6.17
- 操作系统 Windows/Linux

### 项目依赖

```
lxml==4.4.1
fake_useragent==0.1.11
Scrapy==1.6.0
pymongo==3.10.1
```

### 使用说明

#### 1.下载程序

```
git clone git@github.com:CharesFang/Tiny-Weibo-Spider.git
cd Tiny-Weibo-Spider
pip install -r requirements.txt
```

#### 2.数据库配置

1. 创建一个MongoDB数据库，在云服务器、虚拟机或者docker里都可。
2. 进入创建的数据库中，并创建以下集合或者根据自己的需求修改`pipelines.py`中的相关代码。（其实数据库结构还可以继续优化，不过以后再说吧hh）
   - user：存储用户账户数据
   - post：存储用户博文数据
   - follows：存储用户关注者数据
   - followers：存储用户粉丝数据
   - hot_search：存储实时热搜数据
   - key_words：存储根据关键词爬取到的用户博文数据
   - total_num：存储用户发布的博文总数
3. 在 `WeiboSpider`文件夹下有一个`database_tool.py`文件，根据自己的数据库配置完善`DBConnector`类。

#### 3.代理配置

1. 可以修改`settings.py`，将代理与UA中间件禁用，若如此设置，爬虫将不会为每个请求添加代理与UA。

   ```python
   DOWNLOADER_MIDDLEWARES = {
       # 禁用Scrapy自带的代理中间件与UA中间件，启用用户自定义的中间件
       'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
       'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
       # 'WeiboSpider.middlewares.RandomUaAndProxyIpMiddleware': 400,
       'WeiboSpider.middlewares.RandomUaAndProxyIpMiddleware': None,
       'WeiboSpider.middlewares.RetryMiddleware': 544,
   }
   ```

2. 启用`settings.py`中的`RandomUaAndProxyIpMiddleware`中间件，为每个请求添加代理与UA，配置信息如下：

   ```python
   DOWNLOADER_MIDDLEWARES = {
       # 禁用Scrapy自带的代理中间件与UA中间件，启用用户自定义的中间件
       'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
       'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
       'WeiboSpider.middlewares.RandomUaAndProxyIpMiddleware': 400,
       # 'WeiboSpider.middlewares.RandomUaAndProxyIpMiddleware': None,
       'WeiboSpider.middlewares.RetryMiddleware': 544,
   }
   ```

   然后修改`middlewares.py`中的`RandomUaAndProxyIpMiddleware`类，重写`get_proxy_ip`方法，每次返回一条代理IP信息，形如`https://xxx.xxx.xxx.xxx:xxxx`，并修改`process_request`方法为如下；

   ```python
   def process_request(self, request, spider):
       proxy = RandomUaAndProxyIpMiddleware.get_proxy_ip(self.ip_num)
       request.meta['proxy'] = proxy
       request.headers['User-agent'] = self.ua.random
   ```

3. 其实这一部分代码感觉耦合程度有点高，后面再修改吧，改起来稍微繁琐了一点，但也不是不能用（滑稽）

#### 4.运行

##### 程序运行

1. 直接输入命令`scrapy crawl WeiboSpider -a uid=xxxxxxxx`等，输入爬虫必要运行参数，运行对应爬虫。
2. 执行名 `python main.py`，根据提示输入对应的爬虫命令与参数，同样调用相应的爬虫

##### 参数说明

本项目内置每个爬虫的对应参数说明如下表所示。

| 爬虫名称        | 参数说明                                                     |
| --------------- | ------------------------------------------------------------ |
| WeiboSpdier     | uid：目标用户uid，多个uid之间以 '\|' 分隔，不能为空；page：爬取用户博文页数，默认为3 |
| FansListSpider  | uids：目标用户uid，多个uid之间以 '\|' 分割；fans_end：粉丝列表爬取页数，默认10；follows_end：关注列表爬取页数，默认10 |
| HotSearchSpider | 无                                                           |
| KeyWordsSpider  | keywords：爬取关键词，不能为空；page_num，爬取页数，默认为5  |

