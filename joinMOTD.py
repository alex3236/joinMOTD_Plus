import requests
import json
from mcdreforged.api.all import *
# import os
from random import choice
from JsonDataAPI import Json
# from RTextEXP import rtext_formmat

PLUGIN_METADATA = {
    'id': 'join_motd_plus',
    'version': '2.2.2',
    'name': 'joinMOTD++',
    'description': '一个为 MCDR 设计的 MOTD 插件。在玩家进入服务器时展示内容。',
    'dependencies': {
        'json_data_api': '*'
    },
    'author': 'Alex3236',
    'link': 'https://github.com/eagle3236/joinMOTD_Plus'
}

cdn = 'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@latest/sentences/{}.json'
daycount_plugins = ['daycount_nbt']
# daycount_plugins.append('day_count_reforged')
config_folder = 'config/joinMOTD'

def get_day(server: ServerInterface):
    global daycount_plugins
    for i in daycount_plugins:
        try:
            return server.get_plugin_instance(i).getday()
        except Exception:
            pass
    raise ModuleNotFoundError('找不到任何可用的 daycount 实例，请检查是否安装相关插件。')


def load_config(source=None):
    global config
    config = Json('joinMOTD', 'config')
    if not config:
        config["eula"] = False
        config["day_text"] = "今天是§b服务器§r在线的第 §e$day§r 天。"

        config["random_text"] = ["随机字符串1", "随机字符串2"]
        config["random_text_format"] = "[§b随机字符串§r] $random"

        config["hitokoto_type"] = "a"
        config["hitokoto_text"] = "[§b一言§r] $hitokoto"

        config["motd"] = "§e§l$player§r, 欢迎回到§b服务器§r!"

        config["bungee_list"] = {"$子服1": "server1", "子服2": "server2"}
        config["display_list"] = ["motd", "day", "\n", "random_text", "hitokoto", "\n", "bungee_list"]
        config["permission"] = {"!!motd": 3, "!!server": 0}

        config.save()
    if source != None:
    	source.reply('[joinMOTD] 重载配置文件.')
    


def need_download():
    need = False
    try:
        with open(f'{config_folder}/hitokoto.json', 'r') as f:
            if f.read().strip() == '':
                need = True
    except FileNotFoundError:
        need = True
    finally:
        return need


@new_thread('joinMOTD')
def download_hitokoto():
    with open(f'{config_folder}/hitokoto.json', 'w', encoding='utf8') as f:
        f.write(requests.get(cdn.format(config['hitokoto_type'])).text)


def get_local_hitokoto():
    if need_download():
        download_hitokoto()
        return get_local_hitokoto()
    with open(f'{config_folder}/hitokoto.json', 'r', encoding='utf-8') as f:
        i = choice(json.load(f))
        hitokoto_text = config['hitokoto_text']\
            .replace('$hitokoto', i['hitokoto'])\
            .replace('$from', i['from'])\
            .replace('$creator', i['creator'])
    return hitokoto_text


def get_random_text():
    if isinstance(config['random_text'], list):
        return choice(config['random_text'])
    else:
        with open(config['random_text'], 'r', encoding='utf-8') as f:
            lines = [i.strip() for i in f.readlines()]
            return choice(lines)


def get_bungee_text():
    temp = []
    for i in config['bungee_list']:
        if i.startswith('$'):
            temp.append(RTextList('[', RText(i[1:])
                                  .set_color(RColor.aqua)
                                  .set_styles([RStyle.underlined, RStyle.bold])
                                  .set_hover_text('§6当前服务器'), '] '))
        else:
            temp.append(RText(f'[§6{i}§r] ')
                        .set_hover_text(f'点击加入至§6{i}§r')
                        .set_click_event(RAction.run_command, f"/server {config['bungee_list'][i]}"))
    return RTextList(*temp)


def display_motd(server, player, display_list=None):
    text = ['-' * 40]
    if display_list is None:
        display_list = config['display_list']
    for i in config['display_list']:
        if i == 'motd':
            text.append(config['motd'].replace('$player', player))
        elif i == 'day':
            text.append(config['day_text'].replace('$day', str(get_day(server))))
        elif i == 'hitokoto':
            text.append(get_local_hitokoto())
        elif i == 'random_text':
            text.append(config['random_text_format'].replace('$random', get_random_text()))
        elif i == 'bungee_list':
            text.append(get_bungee_text())
        elif i == '\n':
            text.append('')
        else:
            text.append(i)
    text.append('-' * 40)
    for i in text:
        server.tell(player, i)


def display_server_list(source: CommandSource):
    if not source.is_player:
        return
    _ = source
    display_list = ["§e可用的服务器列表：§r", "bungee_list"]
    display_motd(_.get_server(), _.player, display_list)


def is_chinese(string):
    for char in string:
        if u'\u4e00' <= char <= u'\u9fff':
            return True
    return False


def register_command(server: ServerInterface):
    def get_literal_node(literal):
        lvl = config['permission'].get(literal, 0)
        return Literal(literal).requires(lambda src: src.has_permission(lvl), lambda: '权限不足')
    server.register_command(get_literal_node('!!motd').runs(load_config))
    server.register_command(get_literal_node('!!server').runs(display_server_list))
    server.register_help_message('!!motd', '重载 joinMOTD++ 配置文件')
    server.register_help_message('!!server', '显示服务器列表')


def on_load(server: ServerInterface, old):
    load_config()
    register_command(server)
    # if 'hitokoto' not in config['display_list'] and config['eula']:
    #     raise ConnectionAbortedError('EULA 状态为 False。无法开启检查更新/一言功能。') from None
    if need_download():
        server.logger.info('[joinMOTD] 下载一言文件...')
        download_hitokoto()


def on_player_joined(server: ServerInterface, player: str, info: Info):
    try:
        if not is_chinese(player) and not player.startswith('bot_'):
            display_motd(server, player)
    except Exception as e:
        server.tell(player, f'很抱歉，joinMOTD++ 出现错误。请尽快联系服务器管理员。错误代码：\n{e}')
        raise
