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
  # add option for all namespaces (-A)
  title = 'all namespaces'
  subtitle = 'all namespaces'
  arg = 'all_ns'
  icon = 'ns'
  items.append(generate_dict(title,subtitle,arg,icon))

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

##############################
#### namespaced resources ####
##############################

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

    if cm.data is None:
      data_len = 0
    else:
      data_len = len(cm.data)
    
    subtitle = 'Data: {}'.format(data_len)
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

    if sc.data is None:
      data_len = 0
    else:
      data_len = len(sc.data)

    subtitle = 'Type: {}, Data: {}'.format(sc.type,data_len)
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

##########################################
#### resources across all namesapaces ####
##########################################
  
def get_all_pods():
  # generate list of pods in all namespaces

  # get pods
  kubernetes_config()
  api = client.CoreV1Api()
  pods = api.list_pod_for_all_namespaces()

  items = []
  for pod in pods.items:
    title = pod.metadata.name
    arg = '{}/{}'.format(pod.metadata.name,pod.metadata.namespace)
    icon = 'pod'
    subtitle = 'Status: {}, Namespace: {}, Restarts: {}'.format(pod.status.phase,pod.metadata.namespace,pod.status.container_statuses[0].restart_count)
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No pods found'
    subtitle = 'No pods found'
    arg = 'none/none'
    icon = 'pod'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_all_deployments():
  # generate list of deployments in namespace

  # get deployments
  kubernetes_config()
  api = client.AppsV1Api()
  deployments = api.list_deployment_for_all_namespaces()

  items = []
  for dp in deployments.items:
    title = dp.metadata.name
    subtitle = 'Ready: {}/{}, Namespace: {}'.format(dp.status.ready_replicas,dp.status.replicas,dp.metadata.namespace)
    arg = '{}/{}'.format(dp.metadata.name,dp.metadata.namespace)
    icon = 'deploy'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No deployments found'
    subtitle = 'No deployments found'
    arg = 'none/none'
    icon = 'deploy'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_all_configmaps():
  # generate list of configmaps in namespace

  # get deployments
  kubernetes_config()
  api = client.CoreV1Api()
  configmaps = api.list_config_map_for_all_namespaces()
  
  items = []
  for cm in configmaps.items:
    title = cm.metadata.name

    if cm.data is None:
      data_len = 0
    else:
      data_len = len(cm.data)
    
    subtitle = 'Data: {}, Namespace {}'.format(data_len,cm.metadata.namespace)
    arg = '{}/{}'.format(cm.metadata.name,cm.metadata.namespace)
    icon = 'cm'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No configmaps found'
    subtitle = 'No configmaps found'
    arg = 'none/none'
    icon = 'cm'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_all_secrets():
  # generate list of secrets in namespace

  # get secrets
  kubernetes_config()
  api = client.CoreV1Api()
  secrets = api.list_secret_for_all_namespaces()
  
  items = []
  for sc in secrets.items:
    title = sc.metadata.name

    if sc.data is None:
      data_len = 0
    else:
      data_len = len(sc.data)

    subtitle = 'Type: {}, Data: {}'.format(sc.type,data_len)
    arg = '{}/{}'.format(sc.metadata.name,sc.metadata.namespace)
    icon = 'secret'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No secrets found'
    subtitle = 'No secrets found'
    arg = 'none/none'
    icon = 'secret'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_all_statefulsets():
  # generate list of statefulsets in namespace

  # get statefulsets
  kubernetes_config()
  api = client.AppsV1Api()
  statefulsets = api.list_stateful_set_for_all_namespaces()

  # create output list
  items = []
  for sts in statefulsets.items:
    title = sts.metadata.name
    subtitle = 'Ready: {}/{}, Namespace: {}'.format(sts.status.ready_replicas,sts.status.replicas, sts.metadata.namespace)
    arg = '{}/{}'.format(sts.metadata.name,sts.metadata.namespace)
    icon = 'sts'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No statefulsets found'
    subtitle = 'No statefulsets found'
    arg = 'none/none'
    icon = 'sts'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def get_all_pvcs():
  # generate list of PVCs in namespace

  # get PVCs
  kubernetes_config()
  api = client.CoreV1Api()
  pvcs = api.list_persistent_volume_claim_for_all_namespaces()

  # create output list
  items = []
  for pvc in pvcs.items:
    title = pvc.metadata.name
    subtitle = 'Status: {}, Namespace: {}, Volume: {},  Storageclass: {}'.format(pvc.status.phase,pvc.metadata.namespace,pvc.spec.volume_name,pvc.spec.storage_class_name)
    arg = '{}/{}'.format(pvc.metadata.name,pvc.metadata.namespace)
    icon = 'pvc'
    items.append(generate_dict(title,subtitle,arg,icon))

  if len(items) == 0:
    title = 'No PVCs found'
    subtitle = 'No PVCs found'
    arg = 'none/none'
    icon = 'pvc'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

###################
#### Utilities ####
###################
  
def update_context():
  # update the variable kube_context

  contexts, active_context = config.list_kube_config_contexts()

  items = []
  for context in contexts:
    title = context['name']
    subtitle = context['name']
    arg = context['name']
    icon = 'kubernetes'
    items.append(generate_dict(title,subtitle,arg,icon))

  # pass output to Alfred
  sys.stdout.write(generate_json(items))

def kubernetes_config():
  # import global variables to set path to config and context
  kube_config_file = os.getenv('kube_config_path')
  kube_context = os.getenv('kube_context')
  return config.load_kube_config(config_file=kube_config_file,context=kube_context)

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