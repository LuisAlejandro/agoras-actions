#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import chain

from agoras.cli import main


def execute(params):
    expandedparams = [(f'--{k}', v) for k, v in params.items()]
    main(list(chain(['publish'], *expandedparams)))


paramstore = {}
payload = sys.argv[1:]
loopable_actions = ['like', 'share', 'delete']
single_actions = ['post', 'last-from-feed', 'random-from-feed', 'schedule']

for element in payload:
    el = element.split('=', 1)

    if len(el) != 2:
        continue

    param = el[0]
    value = el[1].replace('"', '')

    if not param or not value:
        continue

    paramstore[param] = value

if paramstore['action'] in loopable_actions:

    if paramstore['network'] == 'twitter':
        id_param = 'tweet-id'
    elif paramstore['network'] == 'facebook':
        id_param = 'facebook-post-id'
    elif paramstore['network'] == 'instagram':
        id_param = 'instagram-post-id'
    elif paramstore['network'] == 'linkedin':
        id_param = 'linkedin-post-id'
    else:
        raise Exception(f"Invalid network \"{paramstore['network']}\"")

    for post_id in paramstore[id_param].split(','):
        paramstore[id_param] = post_id
        execute(paramstore)

elif paramstore["action"] in single_actions:
    execute(paramstore)

else:
    raise Exception(f"Invalid action \"{paramstore['action']}\"")
