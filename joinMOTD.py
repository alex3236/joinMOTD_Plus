import requests
import json
from mcdreforged.api.all import *
import os
from random import choice
from JsonDataAPI import Json
from RTextEXP import rtext_formmat

PLUGIN_METADATA = {
    'id': 'join_motd_plus',
    'version': '2.1.0',
    'name': 'joinMOTD++',
    'description': '一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。',
    'dependencies': {
        'json_data_api': '*',
        'rtext_exp': '*'
    },
    'author': 'Alex3236',
    'link': 'https://github.com/eagle3236/joinMOTD_Plus'
}

config = Json('joinMOTD', 'config')
config_folder = 'config/joinMOTD'
cdn = 'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@latest/sentences/{}.json'
daycount_plugins = ['daycount', 'day_count_reforged', 'daycount_nbt']

def get_day(server: ServerInterface):
    global daycount_plugins
    for i in daycount_plugins:
        try:
            return server.get_plugin_instance(i).getday()
        except:
            pass
    raise ModuleNotFoundError('找不到任何可用的 daycount 实例，请检查是否安装相关插件。')


def load_config():
    global config
    if config == {}:
        config["eula"] = False
        config["day_text"] = "今天是服务器在线的第//$day||%c='yellow' %s='bold'//天。"
        
        config["random_text"] = ["随机字符串1", "随机字符串2"]
        config["random_text_format"] = "[//随机字符串||%c='equa' %s='bold'//] $random"

        config["hitokoto_type"] = "a"
        config["hitokoto_text"] = "[//一言||%c='equa' %s='bold'//] $hitokoto"

        config["motd"] = "$player||%c='yellow' %s='bold'//,欢迎回到//服务器||%c='yellow'//!" 

        config["bungee_list"] = {"$子服1": "server1",  "子服2": "server2"}
        config["display_list"] = ["motd", "day", "random_text", "hitokoto", "bungee_list"]
        
        config.save()


def need_download():
    global config_folder
    need_download = False
    try:
        with open(f'{config_folder}/hitokoto.json', 'r') as f:
            if f.read().strip() == '':
                need_download = True
    except FileNotFoundError:
        need_download = True
    finally:
        return need_download


@new_thread('joinMOTD')
def download_hitokoto():
    global config_folder
    with open(f'{config_folder}/hitokoto.json', 'w', encoding='utf8') as f:
        f.write(requests.get(cdn.format(config['hitokoto_type'])).text)

def get_local_hitokoto():
    global config, config_folder
    if need_download():
        download_hitokoto()
        return get_local_hitokoto()
    with open(f'{config_folder}/hitokoto.json', 'r', encoding='utf-8') as f:
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


def display_motd(server, player):
    global config
    text = ['-' * 40]
    for i in config['display_list']:
        if i == 'motd':
            text.append(rtext_formmat(config['motd'].replace('$player', player)))
        elif i == 'day':
            text.append(rtext_formmat(config['day_text'].replace('$day', str(get_day(server)))))
        elif i == 'hitokoto':
            text.append(get_local_hitokoto())
        elif i == 'random_text':
            text.append(rtext_formmat(config['random_text_format'].replace('$random', get_random_text())))
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
    if not 'hitokoto' in config['display_list'] and config['eula']:
        raise ConnectionAbortedError('EULA 状态为 False。无法开启检查更新/一言功能。') from None
    if need_download():
        server.logger.info('[joinMOTD]下载一言文件...')
        download_hitokoto()
    


def on_player_joined(server: ServerInterface, player: str, info: Info):
    try:
        if not is_chinese(player) and not player.startswith('bot_'):
            display_motd(server, player)
    except Exception as e:
        server.tell(player, f'很抱歉，joinMOTD++出现错误。请联系服务器管理员。错误代码：\n{e}')
        raise
