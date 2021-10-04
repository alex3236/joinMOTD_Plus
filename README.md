# joinMOTD++  
一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。  

## 前置安装
1.前置插件
- [JsonDataAPI](https://github.com/zhang-anzhi/MCDReforgedPlugins/tree/master/Archive/JsonDataAPI)：读写配置文件 
- [daycount-NBT](https://github.com/eagle3236/daycount-NBT)：读取开服日期  

2.前置第三方库 `requests`：下载一言
- 使用 `(python -m) pip install requests` 安装即可

## 插件效果
可能与当前版本的效果存在些许差别。
![插件效果](https://ftp.bmp.ovh/imgs/2021/02/7101604f12ce5a99.png)

## 指令
`!!motd`: 重载配置文件。  
`!!server`: 显示服务器列表。

## 配置文件
第一次运行时，应该生成配置文件 **config/joinMOTD/config.json**。该文件内容如下：
```json
{
    "day_text": "今天是§b服务器§r在线的第 §e$day§r 天。",
    "random_text": ["随机字符串1", "随机字符串2"],
    "random_text_format": "[§b随机字符串§r] $random",
    "hitokoto_type": "a",
    "hitokoto_text": "[§b一言§r] $hitokoto",
    "motd": "§e§l$player§r, 欢迎回到§b服务器§r!" ,
    "bungee_list": {
        "$子服1": "server1", 
        "子服2": "server2"
    },
    
    "display_list": [
        "motd",
        "day", "\n",
        "random_text",
        "hitokoto", "\n",
        "bungee_list"
    ],
    "permission": {
      "!!motd": 3,
      "!!server": 0
    }
}
```

### 配置项
`motd`: MOTD欢迎语内容。 **$player** 代表玩家ID。  
 
`day_text`: 开服天数的显示格式。 **$day** 代表天数。  

`random_text`: 自定义随机句子。可以是一个位于 **config/joinMOTD** 文件夹的文件名，或一个字符串列表。若为文件名，则该文件格式应为**每行一个自定义句子**。  
`random_text_format`：随机句子格式。 **$random** 代表句子。

`hitokoto_type`: 一言类型。详见 [一言 相关说明](Hitokoto.md)。  
`hitokoto_text`: 一言格式。详见 [一言 相关说明](Hitokoto.md)。
  
`bungee_list`: BC服务器列表。在子服名称前加 `$` 表示玩家当前所在的子服。  
`display_list`: 信息显示列表。将按照列表顺序依次显示数据。详见下方说明部分。

`permission`: 指令执行所需权限。


### 信息显示列表 可用选项
`motd`: 显示MOTD欢迎语。  
`day`: 显示开服天数。需要 [daycount-NBT](https://github.com/eagle3236/daycount-NBT) ~~或[daycountR](https://github.com/Van-Involution/DayCountR)~~ 插件作为前置。  
`hitokoto`: 显示一言。  
`random_list`: 显示自定义随机句子。  
`bungee_list`: 显示BungeeCord 子服列表。  
`\n`：额外的换行，即显示一个空行，可用作分割线。  
`任意字符`: 将字符作为单独一行显示给玩家。


### 颜色格式说明
为了保证兼容性，从 2.1.1 版本起，不再支持 RText 表达式。  
作为替代，请使用 [格式化代码](https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81?variant=zh-sg) 以显示颜色。
