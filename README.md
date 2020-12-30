## RabbitMQ Kubernetes service
### 1. Description
Streaming service with RabbitMQ Operator based on Kubernetes (minikube),
dummy Producer/Consumer Applications run by Python pika framework.

### 2. Pipeline:

producer-app -> exchange(name=people_exchange, type=fanout) -> queue(name=people_queue) -> consumer-app(x3, round-robin)

### 3. Components:
- RabbitMQ Server - 1
- Producer Application - 1
- Consumer Application - 3

### 4. Installation
#### Run minikube
```
minikube start --vm-driver=virtualbox
eval $(minikube docker-env)
```

#### Set namespace
```
kubectl apply -f kubernetes/dev-namespace.yaml
```

#### Deploy rabbitmq
```
# Install RabbitMQ Cluster Operator
kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/download/v1.3.0/cluster-operator.yml

# Create RabbitMQ Instance
kubectl apply -f kubernetes/rabbitmq/rabbitmq-cluster.yaml

# Create ConfigMap of RabbitMQ
kubectl apply -f kubernetes/rabbitmq/rabbitmq-configmap.yaml
```

#### Deploy producer-app
```
docker build \
    --tag producer-app:1.0 \
    --file docker/producer-app.dockerfile .

kubectl apply -f kubernetes/producer-app/deployment.yaml
```

#### Deploy consumer-app
```
docker build \
    --tag consumer-app:1.0 \
    --file docker/consumer-app.dockerfile .

kubectl apply -f kubernetes/consumer-app/deployment.yaml
```