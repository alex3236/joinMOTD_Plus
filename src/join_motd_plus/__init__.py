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


def day(server: ServerInterface):
    try:
        return getattr(server.get_plugin_instance(config.module_settings['day']['plugin']), config.module_settings['day']['entry'])()
    except Exception:
        print('天数获取失败')
        print_exc()
        return server.tr('join_motd_plus.day_failed')


def server_list(server: ServerInterface):
    l = config.module_settings['server_list']
    output = []
    for i in l:
        if i.startswith('$'):
            output.append(RTextList(
                '[',
                RText(i[1:]).h(server.tr('join_motd_plus.current_server')),
                '] '
            ))
        else:
            output.append(RTextList(
                '[',
                RText(i).h(server.tr('join_motd_plus.click_to_join').replace('server', l[i])).c(RAction.run_command, f'/server {l[i]}'),
                '] '
            ))
    return RTextList(*output)


def parse_json(server: ServerInterface, addr, path):
    try:
        #print(addr,  path)
        req = requests.get(addr, timeout=5).text
        # print(req)
    except requests.exceptions:
        print_exc()
        return server.tr('join_motd_plus.json_failed')
    try:
        req_json = json.loads(req)
        for i in path.strip().split('/'):
            req_json = req_json.get(i, dict())
        return req_json
    except ValueError:
        server.logger.error('自定义 Json 解析错误')
        print_exc()
        return req


@new_thread('joinMOTD++')
def update_json_cache(server: ServerInterface):
    global json_cache_lock, json_cache
    acquired = json_cache_lock.acquire(blocking=False)
    if not acquired:
        return
    for i in json_list:
        _ = json_list[i]
        json_cache[i] = RTextList(_['prefix'], ' ', parse_json(server, _['addr'], _['path']))
    json_cache_lock.release()


def get_json(server: ServerInterface, name: str):
    try:
        return json_cache[name]
    except KeyError:
        print_exc()
        return server.tr('join_motd_plus.json_failed')
    finally:
        update_json_cache(server)


def get_random(server: PluginServerInterface, name):
    path = os.path.join(psi.get_data_folder(), name)
    c = config.module_settings['random']
    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf8') as f:
            f.write(DefaultRandom)
    try:
        with open(path, 'r', encoding='utf8') as f:
            output = random.choice(f.readlines()).strip()
    except Exception:
        server.log.error('随机文本获取失败')
        print_exc()
        output = server.tr('join_motd_plus.random_failed')
    finally:
        return RTextList(c['prefix'], ' ', output)


def display_all(server: ServerInterface, player: str):
    output = ['-'*40]
    for i in config.display_list:
        i = i.strip()
        if i == 'motd':
            output.append(motd(player))
        elif i == 'day':
            output.append(day(server))
        elif i == 'server_list':
            output.append(server_list(server))
        elif i.startswith('json'):
            output.append(get_json(server, i.split(':')[1]))
        elif i.startswith('random'):
            output.append(get_random(server, i.split(':')[1]))
        else:
            output.append(i)
    output.append('-'*40)
    
    for i in output:
        server.tell(player, i)


def display_servers(server: ServerInterface, player: str):
    output = [
        # '-'*40,
        '',
        server_list(server),
        '',
        # '-'*40
    ]
    for i in output:
        server.tell(player, i)


def on_player_joined(server: ServerInterface, player: str, info: Info):
    display_all(server,  player)


def load_config(server: PluginServerInterface, source: CommandSource or None = None):
    global config, json_list
    config = psi.load_config_simple(target_class=Configure, in_data_folder=True, source_to_reply=source)
    json_list = psi.load_config_simple(file_name='json_list.json', default_config=JsonList,
                                       in_data_folder=True, source_to_reply=None)


def register_command(server: PluginServerInterface):
    def get_literal_node(literal):
        lvl = config.permission.get(literal, 0)
        return Literal(literal).requires(lambda src: src.has_permission(lvl), lambda: server.tr('join_motd_plus.perm_denied'))
    server.register_command(get_literal_node('!!reload-motd').runs(lambda src: load_config(src.get_server(), src)))
    server.register_command(get_literal_node('!!motd').runs(lambda src: display_all(
        src.get_server(), src.player)).then(get_literal_node('reload').runs(load_config)))
    server.register_command(get_literal_node('!!server').runs(
        lambda src: display_servers(src.get_server(), src.player)))
    server.register_help_message('!!motd [reload]', server.tr('join_motd_plus.help_motd'))
    server.register_help_message('!!server', server.tr('join_motd_plus.help_server'))


def on_load(server: PluginServerInterface, prev):
    global data_folder, psi
    psi = server
    load_config(server)
    register_command(server)
    update_json_cache(server)
