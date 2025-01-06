# Vertical and horizontal autoscaling

## VPA 

#### Implementation steps

1. Clone the VPA source code from kubernetes official github.

> git clone https://github.com/kubernetes/autoscaler.git

2. deploy using the script

> ./vpa-up.sh

3. deploy vpa controller and an nginx deployment 

> kubectl create -f nginx-vpa.yaml

> kubectl create -f nginx-vpa-deploy.yaml 

#### Observations & Verification

We succesffully created a VPA Recommender Pod, which is responsible to  send recommendations of reasonable uses of resources to the VPA Admission Controller pod.

The Admission Controller pod then sets the resource requests and limits on the containers based on historical usage, resource requests of K8 deployments, StatefulSet or DaemonSet and is periodiacally updated by the recommender pod.

Finally the VPA Update is responsible the scale the pods appropriately without causing disruptions to the cluster.

    leopoldschmid@MacBookPro exercise05 % kubectl describe vpa nginx-vpa                           
    Name:         nginx-vpa
    Namespace:    default
    Labels:       <none>
    Annotations:  <none>
    API Version:  autoscaling.k8s.io/v1
    Kind:         VerticalPodAutoscaler
    Metadata:
    Creation Timestamp:  2024-12-26T17:24:15Z
    Generation:          1
    Resource Version:    463212
    UID:                 ce76efc4-8177-4c44-a96f-672e620172d1
    Spec:
    Resource Policy:
        Container Policies:
        Container Name:  *
        Controlled Resources:
            cpu
            memory
        Max Allowed:
            Cpu:     1
            Memory:  500Mi
        Min Allowed:
            Cpu:     100m
            Memory:  50Mi
    Target Ref:
        API Version:  apps/v1
        Kind:         Deployment
        Name:         nginx-vpa
    Status:
    Conditions:
        Last Transition Time:  2024-12-26T17:26:55Z
        Status:                True
        Type:                  RecommendationProvided
    Recommendation:
        Container Recommendations:
        Container Name:  nginx
        Lower Bound:
            Cpu:     510m
            Memory:  262144k
        Target:
            Cpu:     548m
            Memory:  262144k
        Uncapped Target:
            Cpu:     548m
            Memory:  262144k
        Upper Bound:
            Cpu:     679m
            Memory:  262144k

As we can see in the output above the VPA assigns between 100m (100/1000 = 10%) CPU Power and 50Mi (Mebibytes) up to 1 CPU and 500Mi as we specified it inside the `nginx-vpa.yaml`.

By accessing the nginx web server, which is programmed to generate a lot of work, a burst workload increase is caused. Therefore the vpa destroys the current deployment and generates a new deployment with more resources allocated to it.

## HPA

#### Implementation steps

1. For the HPA to work we need to enable the `metics-server`addon in minikube

> minikube addons enable metrics-server

2. deploy an example apache server with intensive workload

> kubectl apply -f https://k8s.io/examples/application/php-apache.yaml

3. create the HPA

> kubectl autoscale deployment php-apache (<-service-name) --cpu-percent=80 --min=1 --max=10  

4. The inital number of replicas can be configured inside the deployment-yaml file

        apiVersion: apps/v1
        kind: Deployment
        metadata:
        name: my-app
        spec:
        replicas: 3  
        selector:
            matchLabels:
            app: my-app

#### Observation & Verification

- see status of HPA

> kubectl get hpa

- generate load 

        kubectl run -it --rm load-generator --image=busybox /bin/sh
        / # while true; do wget -q -O- http://php-apache; done

        kubectl get hpa 
        NAME         REFERENCE               TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
        php-apache   Deployment/php-apache   cpu: 206%/80%   1         10        1          11m

one minute later the HPA increased the replicas to 5. Since the CPU utilization is now down to 82% again, which is close to the target. No further pods are created, even though the number of replicas is below the max number allowed.

        NAME         REFERENCE               TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
        php-apache   Deployment/php-apache   cpu: 82%/80%   1         10        5          12m

5 minutes after stopping the load the number of replicas still stays the same. This behaviour is rational, since creating and deleting pods is always connected to some additional workload. Decreasing the number of replicase due to sudden stop of workload is not recommended.

        leopoldschmid@MacBookPro exercise05 % kubectl get hpa 
        NAME         REFERENCE               TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
        php-apache   Deployment/php-apache   cpu: 33%/80%   1         10        5          15m
        leopoldschmid@MacBookPro exercise05 % kubectl get hpa 
        NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
        php-apache   Deployment/php-apache   cpu: 0%/80%   1         10        5          18m


After about 10 minutes the HPA downscaled the number of replicas down to 1 again

        leopoldschmid@MacBookPro exercise05 % kubectl get hpa 
        NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
        php-apache   Deployment/php-apache   cpu: 0%/80%   1         10        1          21m

