[中文](https://github.com/eagle3236/joinMOTD_Plus) | **English**

# joinMOTD++

[![](https://pic.stackoverflow.wiki/uploadImages/117/24/20/154/2021/08/24/23/08/8cd61849-6a34-4e2d-ad3a-c6056adef05e.svg)](https://github.com/Fallen-Breath/MCDReforged)

A MOTD plugin designed for MCDR. Displays content when a player enters the server.

## Note

English version of README file is translated by DeepL. If there are any syntax errors, please submit an issue.

## Dependents

1. MCDR

- MCDReforged >= 2.0.1

2. MCDR Plugin

- Any plugin that can output the text of server days, see later for details. Such as[daycount-NBT](https://github.com/eagle3236/daycount-NBT).

3. Third-party libraries

- `requests` (to implement custom online Json functionality)

## Plugin effect

There may be a slight difference with the latest version of the effect.

![插件效果](https://upload.cc/i1/2021/08/24/t6OjbN.png)

## Directive

`!!motd`: Show MOTD.

`!!motd reload`: Reload the plugin.

`!!server`: Show the list of servers.

## Configuration file

The first time the plugin is run, it generates the configuration file **config/join_motd_plus/config.json**. The contents of this file are as follows:

```json5
{
    "permission": { // 指令权限
        "motd": 0,
        "reload": 3, 
        "server": 0
    },
    "display_list": [ // 显示列表
        "motd", // 欢迎消息
        "day", // 天数信息
        "", // 空行
        "json:hitokoto", // json:方案名称 代表自定义在线 Json 方案
        "random:random.txt", // random:文件名 代表自定义随机文本*
        "[自定义文本] 这是一段没卵用的垃圾话。", // 不符合其他规则的视为自定义固定文本
        "",
        "server_list" // 显示服务器选择列表
    ],
    "module_settings": { // 子模块设置
        "motd": { // 欢迎消息设置
            "text": "§e§l$player§r, 欢迎回到§b服务器§r!"
        },
        "day": { // 天数信息设置
            "plugin": "daycount_nbt", // 用于获取天数消息的插件 ID
            "entry": "get_day_text" // 用于获取天数消息的方法入口*
        },
        "server_list": { // 服务器列表设置
            "$§l子服1": "server1", // 开头为 $ 代表当前服务器
            "§a子服2": "server2"
        },
        "random": { // 随机文本设置
            "prefix": "[§b随机文本§r]" // 前缀*
        }
    }
}
```

### Note

1. `display_list/random`: The corresponding file must be a`UTF-8` file in the same folder as the configuration file, with one sentence per line.
2. `module_settings/day/entry`: must be a parameterless method for the specified plugin that returns formatted day information (e.g. "This is the 5th day of the server").
3. `random/prefix`: This is set as a global prefix. If you want each text to have a different prefix, you can set it to null and add the prefix to the file corresponding to the random text itself.
4. This is highlighted in json5 format to explain the configuration items, the actual configuration format is json, no comments are allowed.

## Custom Online Json

joinMOTD++ supports custom online Json, i.e. fetching the text in Json format from the web and getting the desired value.

When run for the first time, the plugin generates a default configuration file **config/join_motd_plus/json_list.json**.

```json
{
    "hitokoto": {
        "prefix": "[§a一言§r]",
        "addr": "https://v1.hitokoto.cn",
        "path": "hitokoto"
    }
}
```

which defines a custom Json that comes out of the box, the one-word API.

Each configuration is a `dict` with the configuration name as its name.

| Configuration items | type | role                   |
| ------------------- | ---- | :--------------------- |
| prefix              | str  | Prefix for output      |
| addr                | str  | The web address to get |
| path                | str  | Json path              |

### Json path

I believe you can see something by this example.

**Original Json:**

```json
{
    "code":0,
    "message":"0",
    "ttl":1,
    "data":{
        "mid":275212628,
        "name":"Alex3236",
        "face":"http://i2.hdslb.com/bfs/face/3d0ffe0e1b23ccaada1f779d7993226f1db16a75.jpg",
        "sign":"不要因为走得太远，就忘了当初为什么出发。 GIthub@eagle3236",
        "rank":10000,
        "level":5,
        "fans_badge":false,
	"official":{
            "role":0,
            "title":"",
            "desc":"",
            "type":-1
        }
    }
}
```

**Json path:**

```plain
data/official/role
```

**Return value:**

```
0
```

## Color Formatting

All text displayed to the player can be [formatted](https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81) using [the formatting code](https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81) to display colors and special formatting.
