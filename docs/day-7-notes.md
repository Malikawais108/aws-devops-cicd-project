Day 7 – Enabling HTTPS with TLS using NGINX Ingress in Kubernetes
Objective

The objective of Day 7 was to secure the Flask application by enabling HTTPS (TLS/SSL) using NGINX Ingress Controller in Kubernetes. This ensures encrypted communication between clients and the application, which is a production-level DevOps requirement.

Tools & Technologies

Kubernetes (Minikube)

NGINX Ingress Controller

TLS / SSL Certificates

kubectl

Docker

Jenkins (CI/CD execution user)

Project Structure
kubernetes/
├── deployment.yaml
├── service.yaml
├── ingress.yaml
├── ingress-tls.yaml
├── hpa.yaml

Step 1: Generate TLS Certificates

A self-signed SSL certificate was generated for local development and testing.

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout flask-devops.key \
-out flask-devops.crt \
-subj "/CN=flask-devops.local"

Step 2: Create Kubernetes TLS Secret

The generated certificate and private key were stored securely as a Kubernetes TLS secret.

kubectl create secret tls flask-devops-tls \
  --cert=flask-devops.crt \
  --key=flask-devops.key


Verify secret creation:

kubectl get secret flask-devops-tls


Expected output:

NAME               TYPE                DATA
flask-devops-tls   kubernetes.io/tls   2

Step 3: Configure TLS in Ingress

TLS was added to the existing ingress resource instead of creating a new one (best practice).

ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-devops-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx

  tls:
  - hosts:
    - flask-devops.local
    secretName: flask-devops-tls

  rules:
  - host: flask-devops.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-devops-service
            port:
              number: 5000


Apply the ingress:

kubectl apply -f ingress.yaml

Step 4: Verify Ingress and TLS

Check ingress details:

kubectl get ingress
kubectl describe ingress flask-devops-ingress


Expected results:

Ports: 80 and 443

TLS enabled

Secret flask-devops-tls attached

Ingress Class: nginx

Step 5: Test HTTPS Access

Test secure access using curl:

curl -k -H "Host: flask-devops.local" https://<minikube-ip>


Successful response confirms:

HTTPS is working

TLS termination is handled by NGINX Ingress

Traffic is routed correctly to the Flask service

Issues Faced & Resolution
Issue
host and path already defined in ingress

Resolution

Kubernetes allows only one ingress per host/path

TLS configuration must be added to the existing ingress

Duplicate ingress resources were avoided

Outcome

Flask application successfully exposed over HTTPS

TLS configured using Kubernetes Secrets

Secure ingress implemented following production best practices

Key Learnings

TLS secrets are required for HTTPS in Kubernetes

NGINX Ingress handles SSL termination

One ingress resource should manage a single host/path

HTTPS is essential for production-grade DevOps systems

Status

Day 7 – Completed Successfully ✅











MALAK AWAIS
