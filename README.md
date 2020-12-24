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

#### Deploy producer-app
```
docker build \
    --tag producer-app:1.0 \
    --file docker/producer-app.dockerfile apps/producer-app

kubectl apply -f kubernetes/producer-app/deployment.yaml
```