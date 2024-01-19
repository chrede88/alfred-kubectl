#!/usr/bin/python3

import sys, json
from kubernetes import client, config

# not used here
query = sys.argv[1]

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
pvs = api.list_persistent_volume()

# create output list
items = []

for i,pv in enumerate(pvs.items):
  tempdict = {}
  tempdict['title'] = pv.metadata.name
  tempdict['subtitle'] = '{}/{}'.format(pv.spec.claim_ref.namespace,pv.spec.claim_ref.name)
  tempdict['arg'] = pv.metadata.name
  tempdict['icon'] = {'path':'./resources/pv.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No PVs found!'
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)