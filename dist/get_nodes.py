#!/usr/bin/python3

import sys, json
from kubernetes import client, config

# not used here
query = sys.argv[1]

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
nodes = api.list_node()

# create output list
items = []
node_active_index = 0

for node in nodes.items:
  tempdict = {}
  tempdict['title'] = node.metadata.name
  tempdict['icon'] = {'path':'./resources/node.png'}

  for i,cond in enumerate(node.status.conditions):
    if cond.type == 'Ready':
      node_active_index = i

  tempdict['subtitle'] = 'Active: {}, Version: {}'.format(node.status.conditions[node_active_index].status,node.status.node_info.kube_proxy_version)
  tempdict['arg'] = node.metadata.name
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No nodes found!'
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)