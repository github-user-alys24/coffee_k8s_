#!/bin/bash
minikube start

# Navigate into the host file
# Change to your file directory before running
cd /mnt/c/Users/ZzSle/Downloads/coffee
# Copy files into Minikube's file system
minikube cp raw_data/coffee_shop.csv /raw_data/
minikube cp template/index.php /template/

# Navigate into the k8s dir
cd /mnt/c/Users/ZzSle/Downloads/coffee/k8

# Apply Kubernetes manifests
echo "Applying k8s manifests..."
# preprocessing
kubectl apply -f preprocessing-kubemanifest.yaml
# Sleep to ensure that the pods are up and running before forwarding
sleep 90
# Port-forward to localhost
echo "Port-forwarding to localhost..."
kubectl port-forward svc/preprocessing-service 8080:8080 &
# Wait a moment to ensure port-forwarding is established
sleep 7

# training
kubectl apply -f training-kubemanifest.yaml
# Sleep to ensure that the pods are up and running before forwarding
sleep 90
# Port-forward to localhost
echo "Port-forwarding to localhost..."
kubectl port-forward svc/training-service 8082:8082 &
# Wait a moment to ensure port-forwarding is established
sleep 7
# Access the website using curl, to save model into /model
curl http://localhost:8082/gbt

# inference
kubectl apply -f inference-kubemanifest.yaml
# Sleep to ensure that the pods are up and running before forwarding
sleep 90
# Port-forward to localhost
echo "Port-forwarding to localhost..."
kubectl port-forward svc/inference-service 8083:8083 &
# Wait a moment to ensure port-forwarding is established
sleep 7

# prediction
kubectl apply -f prediction-kubemanifest.yaml
# Sleep to ensure that the pods are up and running before forwarding
sleep 90
# Port-forward to localhost
echo "Port-forwarding to localhost..."
kubectl port-forward svc/prediction-service 8084:8084 &
# Wait a moment to ensure port-forwarding is established
sleep 7

# website
kubectl apply -f website.yaml
# Sleep to ensure that the pods are up and running before forwarding
sleep 90
# Port-forward to localhost
echo "Port-forwarding to localhost..."
kubectl port-forward svc/website-service 8081:8081 &
# Wait a moment to ensure port-forwarding is established
sleep 7

# Check pods
kubectl get pods

echo "Completed successfully.."
echo "Access website through localhost:8081"