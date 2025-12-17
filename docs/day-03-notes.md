Flask app deployment on Kubernetes

Pods created: flask-app-xxxxxx

NodePort service flask-app-service

Docker image built for Minikube: flask-devops-app:v1

Commands used:

eval $(minikube docker-env)

docker build -t flask-devops-app:v1 -f docker/Dockerfile .

kubectl apply -f kubernetes/deployment.yaml

kubectl get pods / kubectl get svc

Observations / lessons learned

Why eval $(minikube docker-env) is needed

Why NodePort service works for browser access

How pods pick up the local Docker image


1️⃣ Troubleshooting Notes

Common issues you faced today:

ErrImagePull / ContainerCreating

Cause: Kubernetes couldn’t find the Docker image.

Fix: Use eval $(minikube docker-env) and rebuild the image locally, then redeploy.

Service not routing traffic

Cause: Wrong selector or port mismatch in service.yaml.

Fix: Ensure selector matches deployment labels and port:targetPort are correct.

COPY failed in Docker build

Cause: Wrong path to requirements.txt or Flask app folder.

Fix: Make sure Dockerfile path matches the local project structure.

2️⃣ Interview Mode Points


Why eval $(minikube docker-env)?

So that Minikube uses your local Docker daemon — allows pods to pull your local images.

Why NodePort service?

Exposes pods to host machine / browser.

How Kubernetes finds pods?

Services use selector labels to route traffic.

What happens when deployment updates the image?

Old pods terminate, new pods are created with the new image (rolling update).

Why we build image locally and not pull from Docker Hub?

Minikube can’t pull your private image by default, local build ensures availability.

Difference between Pod, Deployment, and Service?

Pod: single or small group of containers

Deployment: manages pods, ensures desired state

Service: exposes pods, load balances traffic
