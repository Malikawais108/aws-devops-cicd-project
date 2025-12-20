# NGINX Ingress Controller

Installed via Helm to expose applications using Ingress.

## Install
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -f values.yaml
