#!/usr/bin/python3

import sys, json
from kubernetes import client, config

# choosen namespace
namespace = sys.argv[1]

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.AppsV1Api()
deployments = api.list_namespaced_deployment(namespace)

# create output list
items = []

for i,deploy in enumerate(deployments.items):
  tempdict = {}
  tempdict['title'] = deploy.metadata.name
  tempdict['subtitle'] = 'Ready: {}/{}'.format(deploy.status.ready_replicas,deploy.status.replicas)
  tempdict['arg'] = deploy.metadata.name
  tempdict['icon'] = {'path':'./resources/deploy.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No deployments in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)