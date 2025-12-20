
  -f prometheus-values.yaml

helm install grafana grafana/grafana \
  --namespace monitoring \
  -f grafana-values.yaml

    Configured Grafana admin credentials in grafana-values.yaml:

        adminUser: admin

        adminPassword: admin

        NodePort: 30000

2. Verified pods

kubectl get pods -n monitoring

Expected Output:

    Prometheus pods running (prometheus-server)

    Grafana pods running (grafana-xxxxx)

3. Access Grafana

    Port-forward Grafana locally:

kubectl port-forward svc/grafana 30000:80 -n monitoring

    Open browser: http://localhost:30000

    Login using admin credentials.

4. Configure Prometheus data source in Grafana

    Data Source: Prometheus

    URL: http://prometheus-server.monitoring.svc.cluster.local:80

    Access: Server (Default)

5. Create dashboards

    Imported default cluster monitoring dashboards from Grafana library.

    Key visualizations:

        Node CPU and memory usage

        Cluster memory and CPU usage

        Network I/O pressure

        Pods CPU and memory usage

        Cluster filesystem usage

6. System log collection using Promtail

    Installed Promtail as a sidecar to collect system logs:

promtail:
  enabled: true
  extraScrapeConfigs: |
    scrape_configs:
      - job_name: system
        static_configs:
          - targets:
              - localhost
            labels:
              job: varlogs
              __path__: /var/log/*.log

    Logs will be sent to Grafana Loki in future iterations (Loki currently removed from project).

7. Verify metrics

    Prometheus metrics available at:
    http://<prometheus-server-ip>:80/metrics

    Grafana dashboards show cluster-level metrics in real-time.

Tools Used

    Prometheus: Monitoring and metrics collection

    Grafana: Dashboard visualization

    Helm: Package manager for Kubernetes

    Kubernetes: Orchestration of pods and services

    kubectl: Kubernetes CLI for cluster management
