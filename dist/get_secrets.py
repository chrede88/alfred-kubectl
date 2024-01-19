#!/usr/bin/python3

import sys, os, json
from kubernetes import client, config

# choosen namespace
namespace = os.getenv('namespace')

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
secrets = api.list_namespaced_secret(namespace)

# create output list
items = []

for secret in secrets.items:
  tempdict = {}
  tempdict['title'] = secret.metadata.name
  tempdict['subtitle'] = 'Type: {}, Data: {}'.format(secret.type,len(secret.data))
  tempdict['arg'] = secret.metadata.name
  tempdict['icon'] = {'path':'./resources/secret.png'}
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No secrets in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)