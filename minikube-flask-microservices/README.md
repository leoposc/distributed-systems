
## Start cluster with two nodes
`minikube start -n=2`

## Build images
``` 
minikube image build -t user-service ./user_service/ 

minikube image build -t product-service ./product_service/ 

minikube image build -t order-service ./order_service/

minikube image build -t gateway-service ./gateway_service/

minikube image build -t scheduler ./scheduler/
```

## Deploy container
`kubectl apply -f k8s/`

## Access the gateway service
`minikube service gateway-service --url`

`curl $(minikube service gateway-service --url)/aggregated`

## Run Python Scheduler
enter scheduler directory

```
kubectl create secret generic sysdig-token --from-file=./token.txt
kubectl create -f sysdig-account.yaml
kubectl create -f scheduler.yaml
kubectl get pods
```

## Contributions
This application was built by Hendrik Paul Munske, Leopold Schmid and Friedrich Hartmann.
