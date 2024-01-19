#!/usr/bin/python3

import sys, os, json
from kubernetes import client, config

# choosen namespace
namespace = os.getenv('namespace')

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.AppsV1Api()
statefulsets = api.list_namespaced_stateful_set(namespace)

# create output list
items = []

for sts in statefulsets.items:
  tempdict = {}
  tempdict['title'] = sts.metadata.name
  tempdict['subtitle'] = 'Ready: {}/{}'.format(sts.status.ready_replicas,sts.status.replicas)
  tempdict['arg'] = sts.metadata.name
  tempdict['icon'] = {'path':'./resources/sts.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No statefulsets in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)