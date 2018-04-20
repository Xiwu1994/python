# -*- coding: utf-8 -*-

# Scrapy settings for crawl_58 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawl_58'

SPIDER_MODULES = ['crawl_58.spiders']
NEWSPIDER_MODULE = 'crawl_58.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  "Accept": "application/json, text/javascript, */*; q=0.01",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
  "Connection": "keep-alive",
  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
  "Host": "xinyu.58.com",
  "Cookie": 'f=n; f=n; f=n; userid360_xml=4D94F52AD65BEB26C0464916AF4F02E5; id58=c5/njVoXf95DIVyPCWg3Ag==; als=0; wmda_uuid=5758766a3f09543f9cdb6e537ab3443f; wmda_new_uuid=1; gr_user_id=8527264b-3713-4e94-8e2b-b5ff0cee2899; wmda_visited_projects=%3B1731916484865%3B2385390625025%3B1409632296065; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1511494313; Hm_lvt_e15962162366a86a6229038443847be7=1511494314; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1511494322; _ga=GA1.2.715551259.1511490409; 58tj_uuid=8045f5a1-d6bb-4900-b38b-c9e8935b900a; xxzl_deviceid=gbD44awpMChAYuLArwR%2FQLPVU2gZgxAHciTKGGaPaX7Cp93JVo0sWUYtfG3SUIVY; __utmz=253535702.1519702300.4.4.utmcsr=g.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/city; __utma=253535702.715551259.1511490409.1519702300.1523194001.5; __utmc=253535702; new_uv=7; utm_source=; spm=; init_refer=; 58home=xinyu; xinyu=201848212646; f=n; city=xinyu; commontopbar_new_city_info=10115%7C%E6%96%B0%E4%BD%99%7Cxinyu; new_session=0; commontopbar_ipcity=xinyu%7C%E6%96%B0%E4%BD%99%7C0; commontopbar_myfeet_tooltip=end; PPU="UID=54718610951694&UN=txk957dea&TT=81482e6b387cd934f4768164e73e1ba9&PBODY=HBK_vrA5sr6ijZa0q_884k_UvuNq0KaTLJZwPKWbN1UurPwth7y6OT43AGHF_PivFVEhOLGCAwWm8jM_Ha5YskcaUFQ7YxH8P7590tbw3LEP3jSbx4PxeBQiQe1bKw12ysN7w9Bady1QUdpsbiKIn2rzuR7-VbuneSJYM-QLHa4&VER=1"; 58cooper="userid=54718610951694&username=txk957dea&cooperkey=013affd18f45d2990cdbf9c10a9b7622"; www58com="AutoLogin=false&UserID=54718610951694&UserName=txk957dea&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=6132DEA395E09C43A420773C6E4139C6005A87D9F8F2CE94E&Phone=&WltUrl=&UserLoginVer=3FFB2E44A074375AA8C94DBBB4CFE61FE&LT=1523194174052"; xxzl_smartid=50ecdceec790e4b679a134cdaab8902f; ppStore_fingerprint=F35042C0707708F266BD1255416541E5E7DBB7AA32ADA1E2%EF%BC%BF1523194250257'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawl_58.middlewares.Crawl58SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawl_58.middlewares.Crawl58DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'crawl_58.pipelines.Crawl58Pipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
