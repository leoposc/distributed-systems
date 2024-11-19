# Start minikube cluster with 3 pods and an ingress api

Start the minikube cluster

`minikube start`

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

