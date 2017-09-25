import urllib2
import json
import socket
api_server = 'heapster.kube-system.svc.cluster.local'
server_name = socket.gethostname()
base_url = 'http://%s/api/v1/model/namespaces/ambari/pods/%s/metrics/'%(api_server,server_name)
print base_url
metrics = ['cpu/limit','cpu/usage_rate','memory/limit','memory/usage']
metrics_dict = {}
for metric in metrics:
  url = base_url + metric
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  content = response.read()
  decodejson = json.loads(content)
  metrics_array = decodejson['metrics']
  #print metric + ':' + str(metrics_array[len(metrics_array)-1]['value'])
  metrics_dict[metric] = metrics_array[len(metrics_array)-1]['value']
for (d,x) in metrics_dict.items():
  print "key:"+d+",value:"+str(x)
