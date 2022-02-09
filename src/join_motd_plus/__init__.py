import json
import os
import random
from threading import Lock
from traceback import print_exc

import requests
from mcdreforged.api.all import *

from join_motd_plus.defaults import *

config: Configure
psi: PluginServerInterface
json_cache = {}
json_cache_lock = Lock()


def motd(player):
    return config.module_settings['motd']['text'].replace('$player', player)


def day():
    try:
        return getattr(psi.get_plugin_instance(config.module_settings['day']['plugin']), config.module_settings['day']['entry'])()
    except Exception:
        print('天数获取失败')
        print_exc()
        return psi.tr('join_motd_plus.day_failed')


def server_list():
    l = config.module_settings['server_list']
    output = []
    for i in l:
        if i.startswith('$'):
            output.append(RTextList(
                '[',
                RText(i[1:]).h(psi.tr('join_motd_plus.current_server')),
                '] '
            ))
        else:
            output.append(RTextList(
                '[',
                RText(i).h(psi.tr('join_motd_plus.click_to_join').replace(
                    'server', l[i])).c(RAction.run_command, f'/server {l[i]}'),
                '] '
            ))
    return RTextList(*output)


def parse_json(addr, path):
    try:
        req = requests.get(addr, timeout=5).text
    except requests.exceptions:
        print_exc()
        return psi.tr('join_motd_plus.json_failed')
    try:
        req_json = json.loads(req)
        for i in path.strip().split('/'):
            req_json = req_json.get(i, dict())
        return req_json
    except ValueError:
        psi.logger.error('自定义 Json 解析错误')
        print_exc()
        return req


@new_thread('joinMOTD++')
def update_json_cache():
    global json_cache_lock, json_cache, json_list
    acquired = json_cache_lock.acquire(blocking=False)
    if not acquired:
        return
    for i in json_list:
        _ = json_list[i]
        json_cache[i] = RTextList(_['prefix'], ' ', parse_json(_['addr'], _['path']))
    json_cache_lock.release()


def get_json(name: str):
    try:
        return json_cache[name]
    except KeyError:
        print_exc()
        return psi.tr('join_motd_plus.json_failed')
    finally:
        update_json_cache()


def get_random(name):
    path = os.path.join(psi.get_data_folder(), name)
    c = config.module_settings['random']
    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf8') as f:
            f.write(DefaultRandom)
    try:
        with open(path, 'r', encoding='utf8') as f:
            output = random.choice(f.readlines()).strip()
    except Exception:
        psi.log.error('随机文本获取失败')
        print_exc()
        output = psi.tr('join_motd_plus.random_failed')
    finally:
        return RTextList(c['prefix'], ' ', output)


def display_all(player=None):
    output = ['-'*40]
    _player = player if player else 'Console'
    for i in config.display_list:
        i = i.strip()
        if i == 'motd':
            output.append(motd(_player))
        elif i == 'day':
            output.append(day())
        elif i == 'server_list':
            output.append(server_list())
        elif i.startswith('json'):
            output.append(get_json(i.split(':')[1]))
        elif i.startswith('random'):
            output.append(get_random(i.split(':')[1]))
        else:
            output.append(i)
    output.append('-'*40)

    for i in output:
        if player:
            psi.tell(_player, i)
        else:
            tell_console(i)


def display_servers(player: str = None):
    output = server_list()
    if player:
        psi.tell(player, output)
    else:
        tell_console(output)


def tell_console(msg):
    psi.get_plugin_command_source().reply(msg)


def on_player_joined(server: ServerInterface, player: str, info: Info):
    display_all(server, player)


def load_config(source=None):
    global config, json_list
    config = psi.load_config_simple(target_class=Configure, in_data_folder=True, echo_in_console=False)

    with open(os.path.join(psi.get_data_folder(), 'json_list.json'), 'r', encoding='utf8') as f:
        json_list = json.load(f)
    if source:
        source.reply(psi.tr('join_motd_plus.reloaded'))
    update_json_cache()


def register_command():
    def get_literal_node(literal):
        lvl = config.permission.get(literal, 0)
        return Literal(literal).requires(lambda src: src.has_permission(lvl), lambda: psi.tr('join_motd_plus.perm_denied'))
    psi.register_command(get_literal_node('!!motd').runs(
        lambda src: display_all(src.player if src.is_player else None)).then(get_literal_node('reload').runs(load_config)))
    psi.register_command(get_literal_node('!!server').runs(
        lambda src: display_servers(src.player if src.is_player else None)))
    psi.register_help_message('!!motd [reload]', psi.tr('join_motd_plus.help_motd'))
    psi.register_help_message('!!server', psi.tr('join_motd_plus.help_server'))


def on_load(server: PluginServerInterface, prev):
    load_config(server.get_plugin_command_source())
    register_command()
