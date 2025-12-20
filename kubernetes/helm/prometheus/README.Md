# Prometheus (Helm)

Installed using Helm to monitor Kubernetes cluster metrics.

## Features
- Pod CPU & Memory monitoring
- Node metrics
- Alerting enabled

## Install
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus -f values.yaml
