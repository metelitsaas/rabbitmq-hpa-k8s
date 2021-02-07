## RabbitMQ Kubernetes service
### 1. Description
Streaming service with RabbitMQ Operator based on Kubernetes (minikube),
dummy Producer/Consumer Applications run by Python pika framework.

### 2. Pipeline:

producer-app -> exchange(name=people_exchange, type=fanout) 
-> queue(name=people_queue) -> consumer-app(x3, round-robin)

### 3. Components:
- RabbitMQ Server - 1
- Producer Application - 1
- Consumer Application - 3

### 4. Installation
#### Run minikube
```
minikube start --vm-driver=virtualbox --cpus 3
minikube addons enable metrics-server
eval $(minikube docker-env)
```

#### Set namespace
```
kubectl apply -f cluster/kubernetes/dev-namespace.yaml
```

#### Deploy rabbitmq
```
# Install RabbitMQ Cluster Operator
kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/download/v1.3.0/cluster-operator.yml

# Encode base64 password for Secrets
echo -n dev_user | base64 # output: ZGV2X3VzZXI=
echo -n dev_pass | base64 # output: ZGV2X3Bhc3M=

# Create secrets of RabbitMQ
kubectl apply -f cluster/kubernetes/rabbitmq/rabbitmq-secret.yaml

# Encode sha256 password for ConfigMap
PWD_HEX=$(echo -n dev_pass | xxd -p)
SALT_HEX="AB99 73CD" 
HEX="$SALT_HEX $PWD_HEX"
SHA256=$(echo -n $HEX | xxd -r -p | shasum -a 256)
echo "$SALT_HEX $SHA256" | xxd -r -p | base64  # output: q5lzzTONASWgosGBd4yRY8au/Wsu4gjlrq6U/nPz1cBX1lDs

# Create ConfigMap of RabbitMQ
kubectl apply -f cluster/kubernetes/rabbitmq/rabbitmq-configmap.yaml

# Create RabbitMQ Instance
kubectl apply -f cluster/kubernetes/rabbitmq/rabbitmq-cluster.yaml
```

#### Deploy producer-app
```
DOCKER_BUILDKIT=1 docker build \
    --tag producer-app:1.1 \
    --file apps/producer-app/docker/producer-app.dockerfile .

kubectl apply -f apps/producer-app/kubernetes/deployment.yaml
```

#### Deploy consumer-app
```
DOCKER_BUILDKIT=1 docker build \
    --tag consumer-app:1.1 \
    --file apps/consumer-app/docker/consumer-app.dockerfile .

kubectl apply -f apps/consumer-app/kubernetes/deployment.yaml
```