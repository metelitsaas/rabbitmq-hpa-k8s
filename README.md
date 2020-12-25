## RabbitMQ Kubernetes service

#### Run minikube
```
minikube start --vm-driver=virtualbox --memory 4096
eval $(minikube docker-env)
```

#### Set namespace
```
kubectl apply -f kubernetes/dev-namespace.yaml
```

#### Deploy producer-app
```
docker build \
    --tag producer-app:1.0 \
    --file docker/producer-app.dockerfile apps/producer-app

kubectl apply -f kubernetes/producer-app/deployment.yaml
```

#### Deploy RabbitMQ
```
# Install RabbitMQ Cluster Operator
kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/download/v1.3.0/cluster-operator.yml

# Create RabbitMQ Instance
kubectl apply -f kubernetes/rabbitmq/rabbitmq-cluster.yaml
```

#### Check RabbitMQ
```
kubectl -n dev get all -l app.kubernetes.io/name=rabbitmq
```