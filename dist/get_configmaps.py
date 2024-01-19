#!/usr/bin/python3

import sys, os, json
from kubernetes import client, config

# choosen namespace
namespace = os.getenv('namespace')

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
configmaps = api.list_namespaced_config_map(namespace)

# create output list
items = []

for cm in configmaps.items:
  tempdict = {}
  tempdict['title'] = cm.metadata.name
  tempdict['subtitle'] = 'Data: {}'.format(len(cm.data))
  tempdict['arg'] = cm.metadata.name
  tempdict['icon'] = {'path':'./resources/cm.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No configmaps in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)