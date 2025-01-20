# Event-driven application in Minikube utilizing Apache Kafka

### Deploy Kafka in minikube

    kubectl apply -f kafka-broker.yaml
    kubectl apply -f zookeeper.yaml

### Package the application with gradle

        ./gradlew clean build

### Dockerize application and deploy it to kubernetes

        docker build -t order-service:latest .
        docker build -t notification-service:latest . 
