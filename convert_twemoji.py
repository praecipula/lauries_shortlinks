#!/usr/bin/env python

import json
import os
import shutil

with open("./emoji_pretty.json") as f:
    j = json.load(f)
    for emoji in j:
        lowercase_code_point = emoji['unified'].lower()
        print(f"{emoji['name']} | {lowercase_code_point} | {emoji['short_names']}")
        for name in emoji['short_names']:
            if os.path.exists(f'../twemoji/assets/72x72/{lowercase_code_point}.png'):
                print("Exists!")
                shutil.copy2(f'../twemoji/assets/72x72/{lowercase_code_point}.png', f'./assets/img/emoji/{name}.png')
            elif os.path.exists(f'../twemoji/assets/72x72/{lowercase_code_point.replace("-fe0f", "")}.png'):
                print ("Second exists!")
                shutil.copy2(f'../twemoji/assets/72x72/{lowercase_code_point.replace("-fe0f", "")}.png', f'./assets/img/emoji/{name}.png')
