import os
import re
import json
from tqdm import tqdm
from util import parse_line


if __name__ == '__main__':
    dir_path = "D:\\los alamos\\auths"

    users = set()
    computers = set()
    auth_types = set()
    logon_types = set()

    filenames = os.listdir(dir_path)
    for filename in tqdm(filenames):
        if not re.findall("txt$", filename):
            continue
        filepath = os.path.join(dir_path, filename)
        if not os.path.isfile(filepath):
            continue
        f = open(filepath)

        for line in f:
            try:
                values = parse_line(line)
            except AssertionError:
                os.remove(filepath)
                continue

            src_user, dest_user = values['src_user'], values['dest_user']
            src_comp, dest_comp = values['src_comp'], values['dest_comp']
            auth_type, logon_type = values['auth_type'], values['logon_type']

            for user in [src_user, dest_user]:
                if user and user not in users:
                    users.add(user)
            for computer in [src_comp, dest_comp]:
                if computer and computer not in computers:
                    computers.add(computer)
            if auth_type not in auth_types:
                auth_types.add(auth_type)
            if logon_type not in logon_types:
                logon_types.add(logon_type)

    user_map = {name: i for i, name in enumerate(users)}
    computer_map = {name: i for i, name in enumerate(computers)}
    auth_type_map = {name: i for i, name in enumerate(auth_types)}
    logon_type_map = {name: i for i, name in enumerate(logon_types)}

    os.mkdir('maps')
    user_map_json = json.dumps(user_map)
    user_map_f = open("maps/user_map.json", "w")
    user_map_f.write(user_map_json)
    user_map_f.close()

    computer_map_json = json.dumps(computer_map)
    computer_map_f = open("maps/computer_map.json", "w")
    computer_map_f.write(computer_map_json)
    computer_map_f.close()

    auth_type_map_json = json.dumps(auth_type_map)
    auth_type_map_f = open("maps/auth_type_map.json", "w")
    auth_type_map_f.write(auth_type_map_json)
    auth_type_map_f.close()

    logon_type_map_json = json.dumps(logon_type_map)
    logon_type_map_f = open("maps/logon_type_map.json", "w")
    logon_type_map_f.write(logon_type_map_json)
    logon_type_map_f.close()
