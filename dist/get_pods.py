#!/usr/bin/python3

import sys, json
from kubernetes import client, config

# choosen namespace
namespace = sys.argv[1]

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
pods = api.list_namespaced_pod(namespace)

# create output list
items = []

for i,pod in enumerate(pods.items):
  tempdict = {}
  tempdict['title'] = pod.metadata.name
  tempdict['subtitle'] = 'Ready: {}'.format(pod.status.conditions[2].status)
  tempdict['arg'] = pod.metadata.name
  tempdict['icon'] = {'path':'./resources/pod.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No pods in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)