#!/usr/bin/env python

import time
import random
import json

from kubernetes import client, config, watch
from sdcclient import SdcClient

config.load_incluster_config()
v1 = client.CoreV1Api()
sdclient = SdcClient("admin")
sysdig_metric = "net.http.request.time"
metrics = [{ "id": sysdig_metric, "aggregations": { "time": "timeAvg", "group": "avg" } }]

scheduler_name = "sysdigsched"


def get_request_time(hostname):
    hostfilter = "host.hostName = '%s'" % hostname
    start = -60
    end = 0
    sampling = 60
    metricdata = sdclient.get_data(metrics, start, end, sampling, filter=hostfilter)
    # Validate and process the data
    if isinstance(metricdata, list) and len(metricdata) > 1:
        if isinstance(metricdata[1], dict) and 'data' in metricdata[1]:
            try:
                request_time = float(metricdata[1]['data'][0]['d'][0])
                print(f"{hostname} ({sysdig_metric}): {request_time}")
                return request_time
            except (IndexError, KeyError, ValueError) as e:
                print(f"Error processing metric data: {e}")
        else:
            print(f"Unexpected structure in metricdata[1]: {metricdata[1]}")
    else:
        print(f"Unexpected structure for metricdata: {metricdata}")

    # Default return value if metric data is invalid
    return float('inf')  # Assign a high value so this node is deprioritized


def best_request_time(nodes):
    if not nodes:
        return []
    node_times = [get_request_time(hostname) for hostname in nodes]
    best_node = nodes[node_times.index(min(node_times))]
    print("Best node: " + best_node)
    return best_node


def nodes_available():
    ready_nodes = []
    for n in v1.list_node().items:
            for status in n.status.conditions:
                if status.status == "True" and status.type == "Ready":
                    ready_nodes.append(n.metadata.name)
    return ready_nodes


def scheduler(name, node, namespace="default"):
    body=client.V1Binding()
    target=client.V1ObjectReference()
    target.kind="Node"
    target.apiVersion="v1"
    target.name= node
    meta=client.V1ObjectMeta()
    meta.name=name
    body.target=target
    body.metadata=meta
    return v1.create_namespaced_binding(namespace, body)


def main():
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, "default"):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            try:
                print("Scheduling " + event['object'].metadata.name)
                print("Nodes available: " + str(nodes_available()))
                res = scheduler(event['object'].metadata.name, best_request_time(nodes_available()))
            except client.rest.ApiException as e:
                print(json.loads(e.body)['message'])

if __name__ == '__main__':
    main()                                                                                                                                                                 