# Grafana (Helm)

Grafana deployed via Helm and integrated with Prometheus.

## Features
- Kubernetes dashboards
- Pod metrics visualization

## Install
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana -f values.yaml
