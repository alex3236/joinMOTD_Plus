# joinMOTD++  
一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。  
**注意：建议从 Releases 页面下载，而不是直接下载源代码。**


## 前置安装
1.前置插件
- [JsonDataAPI](https://github.com/zhang-anzhi/MCDReforgedPlugins/blob/master/JsonDataAPI): 用于读写配置文件 
- [RTextEXP](https://github.com/eagle3236/rtext-exp)：识别 RText 表达式  
- [daycount-NBT](https://github.com/eagle3236/daycount-NBT) 或 [daycountR](https://github.com/Van-Involution/DayCountR) （**可选**）：读取开服日期  

如果你是从 **Releases 页面** 下载此插件，那么以上前置插件将一同被下载，到手即用；但可能不是最新版本。

2.前置第三方库 `requests`：下载一言
- 使用 `pip install requests` 安装即可。


## 插件效果
![插件效果](https://ftp.bmp.ovh/imgs/2021/02/7101604f12ce5a99.png)


## 配置文件
第一次运行时，应该生成配置文件 **config/joinMOTD/config.json**。该文件默认内容如下:   
```json
{
    "day_text": "今天是服务器在线的第//$day||%c='yellow' %s='bold'//天。",
    "random_text": [],
    "random_text_format": "%c='red'",
    "hitokoto_type": "a",
    "hitokoto_text": "[//一言||%c='equa' %s='bold'//] $hitokoto",
    "motd": "$player||%c='yellow' %s='bold'//,欢迎回到//服务器||%c='yellow'//!" ,
    "bungee_list": {
        "$子服1": "server1", 
        "子服2": "server2"
    },
    
    "display_list": [
        "motd",
        "day",
        "hitokoto",
        "bungee_list"
    ]
}
```


### 配置项
`check_update`: 是否自动检查更新。详见 **eula.txt**。  
`motd`: MOTD欢迎语内容。 **$player** 代表玩家ID。  

`display-days`: 显示开服天数。  
`day_text`: 开服天数的显示格式。 **$day** 代表天数。  

`random_text`: 自定义随机句子。可以是一个位于 **config/joinMOTD** 文件夹的文件名，或一个字符串列表。若为文件名，则该文件格式应为**每行一个自定义句子**。  
`random_text_format`：随机句子格式。 **$random** 代表句子。

`hitokoto_type`: 一言类型。详见 **一言 参数说明** 部分。  
`hitokoto_text`: 一言格式。详见 **一言 格式说明** 部分。
  
`bungee_list`: BC服务器列表。在子服名称前加 `$` 表示玩家当前所在的子服。  
`display_list`: 信息显示列表。将按照列表顺序依次显示数据。详见 **信息现实列表 参数说明** 部分。


### 信息显示列表 参数说明
`motd`: 显示MOTD欢迎语。  
`day`: 显示开服天数。需要 [daycount-NBT(推荐)](https://github.com/eagle3236/daycount-NBT) 或 [daycountR](https://github.com/Van-Involution/DayCountR) 插件作为前置。  
`hitokoto`: 显示一言。  
`random_list`: 显示自定义随机句子。  
`bungee_list`: 显示BungeeCord 子服列表。  


### 一言 参数说明
| 参数  | 说明        |
| ----- | ----------- |
| a     | 动画        |
| b     | 漫画        |
| c     | 游戏        |
| d     | 文学        |
| e     | 原创        |
| f     | 来自网络    |
| g     | 其他        |
| h     | 影视        |
| i     | 诗词        |
| j     | 网易云      |
| k默认 | 哲学        |
| l     | 抖机灵      |
| 其他  | 作为 a 处理 |


### 一言 格式说明
`$hitokoto`: 一言内容（说的啥）  
`$from`: 一言来源（谁说的）  
`$creator`: 一言上传者（谁收集的）  

#### 使用例：
**源JSON**：  
```json
{
    "id": 1,
    "uuid": "9818ecda-9cbf-4f2a-9af8-8136ef39cfcd",
    "hitokoto": "与众不同的生活方式很累人呢，因为找不到借口。",
    "type": "a",
    "from": "幸运星",
    "from_who": null,
    "creator": "跳舞的果果",
    "creator_uid": 0,
    "reviewer": 0,
    "commit_from": "web",
    "created_at": "1468605909",
    "length": 22
  },
```

**hitokoto_text** 参数：
```bash
$hitokoto —— $from \n此一言由网友\"$creator\"提供
```

**最终输出**：
```
与众不同的生活方式很累人呢，因为找不到借口。——幸运星 
此一言由网友"跳舞的果果"提供
```


### RText 说明
`hitokoto_text`，`motd`，`day_text` 和 `random_text` 都支持 RText 表达式。  
详见[表达式说明]()


