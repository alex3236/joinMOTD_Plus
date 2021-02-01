# joinMOTD++  

一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。  
**注意：请从 Releases 页面下载，而不是直接下载源代码。**


## 前置安装

**Windows**: `pip install requests`   
**Linux**: `pip3 install requests`   

## 插件效果

![插件效果](https://ftp.bmp.ovh/imgs/2021/02/7101604f12ce5a99.png)


## 配置文件

配置文件为 **config/joinMOTD** 目录的 **joinMOTD++.json**。该文件默认内容如下:   

```json
{
    "check_update": true,

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
`motd`: MOTD欢迎语内容。 **%player%** 代表玩家ID。  

`display-days`: 显示开服天数。  
`day_text`: 开服天数的显示格式。 **%day%** 代表天数。  

`random_text`: 自定义随机句子。可以是一个位于 **config/joinMOTD** 文件夹的文件名，或一个字符串列表。若为文件名，则该文件格式应为**每行一个自定义句子**。  
`hitokoto_type`: 一言类型。详见 **一言 参数说明** 部分。  
`hitokoto_text`: 一言格式。详见 **一言 格式说明** 部分。

`display-bungee-list`: 显示BC服务器列表。点击可以加入对应服务器。  
`bungee-list`: BC服务器列表。在子服名称前加 `$` 表示玩家当前所在的子服。  
`display_list`: 信息显示列表。将按照列表顺序依次显示数据。支持的数据类型如下：  

### 信息显示列表 参数说明

`motd`: 显示MOTD欢迎语。
`day`: 显示开服天数。需要 [daycount-NBT(推荐)](https://github.com/eagle3236/daycount-NBT) 或 [daycount](https://github.com/TISUnion/daycount) 插件作为前置。
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
$hitokoto —— $from \n此一言来自网友\"$creator\"
```

**输出**：

```bash
与众不同的生活方式很累人呢，因为找不到借口。——幸运星 
此一言来自网友"跳舞的果果"
```



### RText 说明

`hitokoto_text`，`motd`，`day_text` 和 `random_text` 都支持 RText。
**注意**：RText为阉割版，仅支持指定 `hover_text`，`color` 和 `style`。
**另**：尽管使用样式代码似乎更加简单，但样式代码无法设置鼠标悬停文字，且 RText 表达式可以在不看样式表的情况下更快速地辨认和设定样式。请酌情选用——当然，同时用应该也不会有什么大问题 :P

#### 使用方法

这是一个使用了 RText 的 `motd` 参数：

```bash
$player||%c='yellow' %s='bold'//，欢迎回到服务器！||%h='这是鼠标悬停文字' %s='underline bold'
```

其中，`||` 将正常文字与 RText 表达式分开；`// ` 将两个 RText 表达式分开。
**%h** 代表 hover_text，即鼠标悬停文字。
​	**参数**：需要作为悬停文字的字符串

**%s** 代表 RStyle，即文字样式。如需多种样式，请用半角空格作为分割。
​	**可用参数**：`bold`(加粗)  `italic`(斜体)  `underlined`(下划线)  `strikethrough`(删除线)  `obfuscated`(乱码)

**%c** 代表 RColor，即文字颜色。
​	**可用参数**：`black`  `dark_blue`  `dark_green`  `dark_aqua`  `dark_red`  `dark_purple`  `gold`  `gray`  `dark_gray`  `blue`  `green`  `aqua`  `red`  `light_purple`  `yellow`  `white`  `reset`

**注意**：一个表达式中不能同时存在多个相同参数。

综上，这个表达式的最终效果如下：
![RText 效果](https://ftp.bmp.ovh/imgs/2021/02/49b51431621b6f93.png)

