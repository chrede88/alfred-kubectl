#!/usr/bin/python3

import sys, json
from kubernetes import client, config

# not used here
query = sys.argv[1]

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
namespaces = api.list_namespace()

# create output list
items = []

for i,ns in enumerate(namespaces.items):
  tempdict = {}
  tempdict['title'] = 'In {}'.format(ns.metadata.name)
  tempdict['subtitle'] = ns.status.phase
  tempdict['arg'] = ns.metadata.name
  tempdict['icon'] = {'path':'./resources/ns.png'}
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)