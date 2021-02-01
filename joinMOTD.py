import requests
import json
from mcdreforged.api.all import *
import os
from random import choice
from daycount import getday
from re import search

PLUGIN_METADATA = {
    'id': 'join_motd_plus',
    'version': '2.0.0',
    'name': 'joinMOTD++',
    'description': '一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。',
    'author': 'Alex3236',
    'link': 'https://github.com/eagle3236'
}
config = {}
cdn = 'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@latest/sentences/{}.json'


def check_eula():
    with open('config/joinMOTD/eula.txt', 'r', encoding='utf8') as f:
        eula = f.readlines(1)[0].strip()[5:]
    if eula == 'true':
        return True
    elif eula == 'false':
        return False
    else:
        raise SyntaxError('EULA 文件格式错误。请检查 eula.txt。详情请见 https://github.com/eagle3236')


def load_config():
    global config
    with open('config/joinMOTD/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)


@new_thread('joinMOTD')
def download_hitokoto():
    with open('config/joinMOTD/hitokoto.txt', 'w', encoding='utf8') as f:
        f.write(requests.get(cdn.format(f"{config['hitokoto_type']}")).text)


def get_local_hitokoto():
    global config
    if not os.path.exists('config/joinMOTD/hitokoto.txt'):
        download_hitokoto()
        return get_local_hitokoto()
    with open('config/joinMOTD/hitokoto.txt', 'r', encoding='utf-8') as f:
        i = choice(json.load(f))
        hitokoto_text = config['hitokoto_text']\
            .replace('$hitokoto', i['hitokoto'])\
            .replace('$from', i['from'])\
            .replace('$creator', i['creator'])
    return rtext_formmat(hitokoto_text)


def get_random_text():
    global config
    if type(config['random_text']) == list:
        return choice(config['random_text'])
    else:
        with open(config['random_text'], 'r', encoding='utf-8') as f:
            lines = [i.strip() for i in f.readlines()]
            return choice(lines)


def get_bungee_text():
    global config
    temp = ['\n']
    for i in config['bungee_list']:
        if i.startswith('$'):
            temp.append(RTextList('[', RText(i[1:])
                                  .set_color(RColor.aqua).set_styles([RStyle.underlined, RStyle.bold]).set_hover_text(
                '§6当前服务器'), '] '))
        else:
            temp.append(RText(f'[§6{i}§r] ')
                        .set_hover_text(f'点击加入至§6{i}§r')
                        .set_click_event(RAction.run_command, f"/server {config['bungee_list'][i]}"))
    return RTextList(*temp)


def rtext_formmat(text: str, new=True):
    if '||' not in text:
        return text
    if '//' in text:
        rtext_list = []
        for i in text.split('//'):
            rtext_list.append(rtext_formmat(i, new=False))
        rtext_list.append('\n')
        return RTextList(*rtext_list)
    text = text.split('||')
    rtext_express = text[1]
    style = search(r"%s=['\"](.*?)['\"]", rtext_express)
    color = search(r"%c=['\"](.*?)['\"]", rtext_express)
    hover = search(r"%h=['\"](.*?)['\"]", rtext_express)
    text = RText(text[0])
    if style is not None:
        for i in style.group(1).split(' '):
            if i in RStyle.__members__:
                text.set_styles(eval(f'RStyle.{i}'))
    if color is not None:
        color = color.group(1)
        if color in RColor.__members__:
            text.set_color(eval(f'RColor.{color}'))
    if hover is not None:
        text.set_hover_text(hover.group(1))
    return RTextList(text, '\n') if new else text


def display_motd(server, player):
    global config
    text = ['-' * 40]
    for i in config['display_list']:
        if i == 'motd':
            text.append(rtext_formmat(config['motd'].replace('$player', player)))
        elif i == 'day':
            text.append(rtext_formmat(config['day_text'].replace('$day', str(getday()))))
        elif i == 'hitokoto':
            text.append(get_local_hitokoto())
        elif i == 'random_text':
            text.append(rtext_formmat(get_random_text()))
        elif i == 'bungee_list':
            text.append(get_bungee_text())
    text.append('-' * 40)
    for i in text:
        server.tell(player, i)


def is_chinese(string):
    for char in string:
        if u'\u4e00' <= char <= u'\u9fff':
            return True
    return False


def on_load(server: ServerInterface, old):
    global config
    server.register_command(Literal('!!motd').runs(load_config))
    server.register_help_message('!!motd', '重载 joinMOTD++ 配置文件')
    server.logger.info('[joinMOTD]加载配置文件...')
    load_config()
    if not config['check_update'] or 'hitokoto' in config['display_list'] and not check_eula():
        raise ConnectionAbortedError('EULA 状态为 False。无法开启检查更新/一言功能。')
    server.logger.info('[joinMOTD]解析一言文件...')
    get_local_hitokoto()


def on_player_joined(server: ServerInterface, player: str, info: Info):
    try:
        if not is_chinese(player) and not player.startswith('bot_'):
            display_motd(server, player)
    except Exception:
        server.tell(player, '很抱歉，joinMOTD出现错误。请联系服务器管理员')
        raise
