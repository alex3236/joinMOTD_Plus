
# joinMOTD++

[![](https://pic.stackoverflow.wiki/uploadImages/117/24/20/154/2021/08/24/23/08/8cd61849-6a34-4e2d-ad3a-c6056adef05e.svg)](https://github.com/Fallen-Breath/MCDReforged)

一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。

## 前置

1. MCDR

- MCDReforged >= 2.0.1

2. 前置插件

- 任意可以输出开服天数文本的插件，详见后文。如 [daycount-NBT](https://github.com/eagle3236/daycount-NBT)。

3. 前置第三方库

- `requests`（实现自定义在线 Json 功能）

## 插件效果

可能与最新版本的效果存在些许差别。

![插件效果](https://upload.cc/i1/2021/08/24/t6OjbN.png)

## 指令

`!!motd`: 显示 MOTD。

`!!motd reload`: 重载插件。

`!!server`: 显示服务器列表。

## 配置文件

第一次运行时，插件会生成配置文件 **config/join_motd_plus/config.json**。该文件内容如下：

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

### 注意

1. `display_list/random`: 对应的文件必须是一个与配置文件同文件夹的、`UTF-8` 格式的文件，每行一句话。
2. `module_settings/day/entry`: 必须为指定插件的一个无需实参的方法，返回已经经过格式化的天数信息（比如“这是服务器开服的第5天”）。**默认支持 daycount_NBT**
3. `random/prefix`: 此处设置的为全局前缀。如果想让每句文本有不同的前缀，可将其设置为空，并在随机文本对应的文件中自行添加前缀。
4. 此处使用 json5 格式高亮以对配置项进行解释，实际配置格式为 json, 不可使用注释。

## 自定义在线 Json

joinMOTD++ 支持自定义在线 Json, 即从网络上获取 Json 格式的文本并得到所需的值。

第一次运行时，插件会生成默认配置文件 **config/join_motd_plus/json_list.json**：

```json
{
    "hitokoto": {
        "prefix": "[§a一言§r]",
        "addr": "https://v1.hitokoto.cn",
        "path": "hitokoto"
    }
}
```

其中定义了一个开箱自带的自定义 Json, 即一言 API。

每个配置都是以配置名作为名称的 `dict`。

| 配置项 | 类型 | 作用              |
| ------ | ---- | :---------------- |
| prefix | str  | 输出时的前缀      |
| addr   | str  | 要获取的 Web 地址 |
| path   | str  | Json 路径         |

### 预加载

所有自定义在线 Json 都会预加载，以保证最快的响应速度。在插件被加载、缓存被读取后，joinMOTD++ 会更新缓存。


### Json 路径

相信你可以通过这个例子看出些什么：

**原 Json:**

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

**Json 路径:**

```plain
data/official/role
```

**返回值:**

```
0
```

## 颜色格式

所有对玩家显示的文本都可以使用 [格式化代码](https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81) 以显示颜色和特殊格式。
