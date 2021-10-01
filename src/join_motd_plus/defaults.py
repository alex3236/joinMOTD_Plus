from typing import Dict, List
from mcdreforged.api.all import Serializable

class Configure(Serializable):
    permission: Dict[str, int] = {
        'motd': 0,
        'reload': 3,
        'server': 0
    }
    display_list: List[str] = [
        'motd',
        'day',
        '',
        'json:hitokoto',
        'random:random.txt',
        '[自定义文本] 这是一段没卵用的垃圾话。',
        '',
        'server_list',
    ]
    module_settings: Dict[str, dict] = {
        'motd': {
            'text': '§e§l$player§r, 欢迎回到§b服务器§r!'
        },
        'day': {
            'plugin': 'daycount_nbt',
            'entry': 'get_day_text'
        },
        'server_list': {
            '$§l子服1': 'server1',
            '§a子服2': 'server2'
        },
        'json': {
            'preload': True
        },
        'random': {
            'prefix': '[§b随机文本§r]'
        }
    }


JsonList = {
    'hitokoto': {
        'prefix': '[§a一言§r]',
        'addr': 'https://v1.hitokoto.cn',
        'path': 'hitokoto'
    }
}

DefaultRandom = '''
§e§lAlex3236, yyds!
如果你看到了这句话，那么你一定看到了这句话。
记得叫服务器管理员修改随机文本哦 awa
上次看到你这么有意思的人，还是在上次。
阿坝阿巴阿巴？
你知道吗？Github 是全球最大的§m同§r异性交友网站。
这是一句废话。
'''.strip()