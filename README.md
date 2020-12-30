## RabbitMQ Kubernetes service

#### Run minikube
```
minikube start --vm-driver=virtualbox
eval $(minikube docker-env)
```

#### Set namespace
```
kubectl apply -f kubernetes/dev-namespace.yaml
```

#### Deploy RabbitMQ
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