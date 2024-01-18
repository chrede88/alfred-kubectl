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

for i,node in enumerate(nodes.items):
  tempdict = {}
  tempdict['title'] = node.metadata.name
  tempdict['subtitle'] = 'Active: {}, Version: {}'.format(node.status.conditions[3].status,node.status.node_info.kube_proxy_version)
  tempdict['arg'] = node.metadata.name
  tempdict['icon'] = {'path':'./resources/node.png'}
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