import sys, json
from kubernetes import client, config

# not used here
query = sys.argv[1]

# kubernetes config
config.load_kube_config()

# get namespaces
v1 = client.CoreV1Api()
namespaces = v1.list_namespace()

# create output list
items = []

for i,ns in enumerate(namespaces.items):
  tempdict = {}
  tempdict['title'] = ns.metadata.name
  tempdict['subtitle'] = ns.status.phase
  tempdict['arg'] = ns.metadata.name
  tempdict['icon'] = './resources/ns.png'
  items.append(json.dumps(tempdict))

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(items)

# pass output to Alfred
sys.stdout.write(jsonstr)