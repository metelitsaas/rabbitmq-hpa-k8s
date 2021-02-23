## RabbitMQ HorizontalPodAutoscaler Kubernetes
### 1. Description
Streaming service with RabbitMQ Operator based on Kubernetes (minikube). RabbitMQ Metric Server runs by Flask framework
and takes metrics from RabbitMQ REST API. Dummy Producer and Consumer Applications run by Python pika framework.
Horizontal Pod Autoscaler reads queue's messages count from RabbitMQ Metric Server and controls count 
of Consumer App's replicas.

### 2. Pipeline:
producer-app -> exchange(name=people_exchange, type=fanout) 
-> queue(name=people_queue) -> consumer-app(HPA, round-robin)

### 3. Components:
- RabbitMQ Server
- RabbitMQ Metric Server
- Producer Application
- Consumer Application

### 4. Installation
#### Run minikube
```
minikube start --vm-driver=virtualbox --cpus 2
minikube addons enable metrics-server
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

# Encode base64 password for Secrets
echo -n dev_user | base64 # output: ZGV2X3VzZXI=
echo -n dev_pass | base64 # output: ZGV2X3Bhc3M=

# Create secrets of RabbitMQ
kubectl apply -f kubernetes/rabbitmq/rabbitmq-secret.yaml

# Encode sha256 password for ConfigMap
PWD_HEX=$(echo -n dev_pass | xxd -p)
SALT_HEX="AB99 73CD" 
HEX="$SALT_HEX $PWD_HEX"
SHA256=$(echo -n $HEX | xxd -r -p | shasum -a 256)
echo "$SALT_HEX $SHA256" | xxd -r -p | base64  # output: q5lzzTONASWgosGBd4yRY8au/Wsu4gjlrq6U/nPz1cBX1lDs

# Create ConfigMap of RabbitMQ
kubectl apply -f kubernetes/rabbitmq/rabbitmq-configmap.yaml

# Create RabbitMQ Instance
kubectl apply -f kubernetes/rabbitmq/rabbitmq-cluster.yaml

# Create RabbitMQ external service
kubectl apply -f kubernetes/rabbitmq/rabbitmq-service.yaml
```

#### Deploy rabbitmq-metric-server
```
DOCKER_BUILDKIT=1 docker build \
    --tag rabbitmq-metric-server:0.2 \
    --file docker/rabbitmq-metric-server.dockerfile .

kubectl apply -f kubernetes/rabbitmq-metric-server/deployment.yaml
kubectl apply -f kubernetes/rabbitmq-metric-server/service.yaml
kubectl apply -f kubernetes/rabbitmq-metric-server/api-service.yaml
```

#### Deploy producer-app
```
DOCKER_BUILDKIT=1 docker build \
    --tag producer-app:1.2 \
    --file docker/producer-app.dockerfile .

kubectl apply -f kubernetes/producer-app/deployment.yaml
```

#### Deploy consumer-app
```
DOCKER_BUILDKIT=1 docker build \
    --tag consumer-app:1.3 \
    --file docker/consumer-app.dockerfile .

kubectl apply -f kubernetes/consumer-app/deployment.yaml
kubectl apply -f kubernetes/consumer-app/hpa.yaml
```
