# Start minikube cluster with 3 pods and an ingress api

## Getting started with Kubernetes

Start the minikube cluster

`minikube start`

load the docker images into minikube

`minikube image load <image-name>`

The image names in this example are: `search`, `convert` and `music-player`

enable ingress

`minikube addons enable ingress`

Verify that the NGINX Ingress controller is running

` kubectl get pods -n ingress-nginx`

Deploy all 3 pods

```sh
kubectl apply -f music-player.yaml 
kubectl apply -f convert.yaml
kubectl apply -f search.yaml
```

Visit the Service via NodePort, using the `minikube service`command. For macOS

`minikube service <service/deployment-name> --url`

## Use prometheus and grafana for monitoring

Create a namespace for prometheus:

`kubectl create namespace monitoring`

Apply all 3 prometheus yaml files to the monitoring namespace.

#### Grafana


Install grafana. 
```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```


```
leopoldschmid@MacBookPro exercise03 % helm install grafana grafana/grafana --namespace monitoring

NAME: grafana
LAST DEPLOYED: Sun Nov 24 23:20:12 2024
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:

   kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   grafana.monitoring.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
     export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace monitoring port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin
#################################################################################
######   WARNING: Persistence is disabled!!! You will lose your data when   #####
######            the Grafana pod is terminated.                            #####
#################################################################################
```

### Access Grafana

`kubectl get service -n monitoring`

Expose grafana.

`kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-ext`

and generate url by:

`minikube service grafana-ext``

## next step: configure grafana to use prometheus. 
