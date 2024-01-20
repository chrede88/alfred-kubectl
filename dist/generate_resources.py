#!/usr/bin/python3

import sys, json

# resources
resources = ['pod','deployment','statefulset','node','namespace','configmap','secret','pv','pvc']
icons = ['pod','deploy','sts','node','ns','cm','secret','pv','pvc']

# create output list
items = []

for i,rs in enumerate(resources):
  tempdict = {}
  tempdict['title'] = rs
  tempdict['subtitle'] = 'Fetch {} resource'.format(rs)
  tempdict['arg'] = rs
  tempdict['icon'] = {'path':'./resources/{}.png'.format(icons[i])}
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)