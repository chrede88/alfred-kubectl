#!/usr/bin/python3

import sys, json, os
from kubernetes import client, config

def generate_resources():
  # generate json with supported kubernetes resources
  # for the initial script filter
  
  # resources
  resources = ['pod','deployment','statefulset','node','namespace','configmap','secret','pv','pvc']
  icons = ['pod','deploy','sts','node','ns','cm','secret','pv','pvc']

  items = []
  for i,rs in enumerate(resources):
    title = rs
    subtitle = 'Fetch {} resource'.format(rs)
    arg = rs
    items.append(generate_dict(title,subtitle,arg,icons[i]))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_namespaces():
  # generate list of namespaces

  # get namespaces
  kubernetes_config()
  api = client.CoreV1Api()
  namespaces = api.list_namespace()

  items = []
  for ns in namespaces.items:
    title = ns.metadata.name
    subtitle = ns.status.phase
    arg = ns.metadata.name
    icon = 'ns'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_nodes():
  # generate list of nodes

  # get nodes
  kubernetes_config()
  api = client.CoreV1Api()
  nodes = api.list_node()

  items = []
  node_active_index = 0
  for node in nodes.items:
    title = node.metadata.name
    arg = node.metadata.name
    icon = 'node'

    for i,cond in enumerate(node.status.conditions):
      if cond.type == 'Ready':
        node_active_index = i

    subtitle = 'Active: {}, Version: {}'.format(node.status.conditions[node_active_index].status,node.status.node_info.kube_proxy_version)
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_pvs():
  # generate list of PVs

  # get PVs
  kubernetes_config()
  api = client.CoreV1Api()
  pvs = api.list_persistent_volume()

  items = []
  for pv in pvs.items:
    title = pv.metadata.name
    subtitle = 'namespace: {}, ref: {}, storageclass: {}'.format(pv.spec.claim_ref.namespace,pv.spec.claim_ref.name,pv.spec.storage_class_name)
    arg = pv.metadata.name
    icon = 'pv'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No PVs found!'
    subtitle = 'No PVs found!'
    arg = 'none'
    icon = 'pv'
    items.append(generate_dict(title,subtitle,arg,icon))
  
  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_pods():
  # generate list of pods in namespace

  # choosen namespace
  namespace = os.getenv('namespace')

  # get pods
  kubernetes_config()
  api = client.CoreV1Api()
  pods = api.list_namespaced_pod(namespace)

  items = []
  for pod in pods.items:
    title = pod.metadata.name
    arg = pod.metadata.name
    icon = 'pod'
    subtitle = 'Status: {}, Restarts: {}'.format(pod.status.phase,pod.status.container_statuses[0].restart_count)
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No pods in {}'.format(namespace)
    subtitle = 'No pods in {}'.format(namespace)
    arg = 'none'
    icon = 'pod'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_deployments():
  # generate list of deployments in namespace
  
  # choosen namespace
  namespace = os.getenv('namespace')

  # get deployments
  kubernetes_config()
  api = client.AppsV1Api()
  deployments = api.list_namespaced_deployment(namespace)

  items = []
  for dp in deployments.items:
    title = dp.metadata.name
    subtitle = 'Ready: {}/{}'.format(dp.status.ready_replicas,dp.status.replicas)
    arg = dp.metadata.name
    icon = 'deploy'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No deployments in {}'.format(namespace)
    subtitle = 'No deployments in {}'.format(namespace)
    arg = 'none'
    icon = 'deploy'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_configmaps():
  # generate list of configmaps in namespace
  
  # choosen namespace
  namespace = os.getenv('namespace')

  # get deployments
  kubernetes_config()
  api = client.CoreV1Api()
  configmaps = api.list_namespaced_config_map(namespace)
  
  items = []
  for cm in configmaps.items:
    title = cm.metadata.name
    subtitle = 'Data: {}'.format(len(cm.data))
    arg = cm.metadata.name
    icon = 'cm'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No configmaps in {}'.format(namespace)
    subtitle = 'No configmaps in {}'.format(namespace)
    arg = 'none'
    icon = 'cm'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_secrets():
  # generate list of secrets in namespace
  
  # choosen namespace
  namespace = os.getenv('namespace')

  # get secrets
  kubernetes_config()
  api = client.CoreV1Api()
  secrets = api.list_namespaced_secret(namespace)
  
  items = []
  for sc in secrets.items:
    title = sc.metadata.name
    subtitle = 'Type: {}, Data: {}'.format(sc.type,len(sc.data))
    arg = sc.metadata.name
    icon = 'secret'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No secrets in {}'.format(namespace)
    subtitle = 'No secrets in {}'.format(namespace)
    arg = 'none'
    icon = 'secret'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_statefulsets():
  # generate list of statefulsets in namespace
  
  # choosen namespace
  namespace = os.getenv('namespace')

  # get statefulsets
  kubernetes_config()
  api = client.AppsV1Api()
  statefulsets = api.list_namespaced_stateful_set(namespace)

  # create output list
  items = []

  for sts in statefulsets.items:
    title = sts.metadata.name
    subtitle = 'Ready: {}/{}'.format(sts.status.ready_replicas,sts.status.replicas)
    arg = sts.metadata.name
    icon = 'sts'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No statefulsets in {}'.format(namespace)
    subtitle = 'No statefulsets in {}'.format(namespace)
    arg = 'none'
    icon = 'sts'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_pvcs():
  # generate list of PVCs in namespace
  
  # choosen namespace
  namespace = os.getenv('namespace')

  # get PVCs
  kubernetes_config()
  api = client.CoreV1Api()
  pvcs = api.list_namespaced_persistent_volume_claim(namespace)

  # create output list
  items = []

  for pvc in pvcs.items:
    title = pvc.metadata.name
    subtitle = 'Status: {}, Storageclass: {}, Volume: {}'.format(pvc.status.phase,pvc.spec.storage_class_name,pvc.spec.volume_name)
    arg = pvc.metadata.name
    icon = 'pvc'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No PVCs in {}'.format(namespace)
    subtitle = 'No PVCs in {}'.format(namespace)
    arg = 'none'
    icon = 'pvc'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

###################
#### Utilities ####
###################

def kubernetes_config():
  # import global variable to set path to config
  kube_config_file = os.getenv('kube_config_path')
  return config.load_kube_config(config_file=kube_config_file)

def generate_json(items_list):
  # generate json output from list of dicts
  jsondict = {}
  jsondict['items'] = items_list
  return json.dumps(jsondict)

def generate_dict(title,subtitle,arg,icon):
  # generate single entry of output
  tempdict = {}
  tempdict['title'] = title
  tempdict['subtitle'] = subtitle
  tempdict['arg'] = arg
  tempdict['icon'] = {'path':'./resources/{}.png'.format(icon)}

  return tempdict

if __name__ == '__main__':
    globals()[sys.argv[1]]()