#!/usr/bin/python3

import sys, os, json
from kubernetes import client, config

# choosen namespace
namespace = os.getenv('namespace')

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
pvcs = api.list_namespaced_persistent_volume_claim(namespace)

# create output list
items = []

for pvc in pvcs.items:
  tempdict = {}
  tempdict['title'] = pvc.metadata.name
  tempdict['subtitle'] = 'Status: {}, Storageclass: {}, Volume: {}'.format(pvc.status.phase,pvc.spec.storage_class_name,pvc.spec.volume_name)
  tempdict['arg'] = pvc.metadata.name
  tempdict['icon'] = {'path':'./resources/pvc.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No PVCs in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)