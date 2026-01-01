Day 10 – GitOps Auto-Healing with ArgoCD
Project

Enterprise GitOps CI/CD Platform for Cloud-Native Microservices

🎯 Objective

To validate self-healing, automated synchronization, and Git as Single Source of Truth using ArgoCD by:

Breaking application state manually

Observing drift

Fixing configuration in Git

Letting ArgoCD automatically reconcile the cluster

🛠 Tools Used

| Category         | Tools          |
| ---------------- | -------------- |
| CI/CD            | Jenkins        |
| Containerization | Docker         |
| Registry         | DockerHub      |
| SCM              | GitHub         |
| GitOps CD        | ArgoCD         |
| Orchestration    | Kubernetes     |
| OS               | Ubuntu Linux   |
| App              | Flask (Python) |


Pre-Requirements

Jenkins pipeline pushing images to DockerHub

Kubernetes deployment managed via GitHub

ArgoCD installed and application created

Auto-sync enabled:

Pre-Requirements

Jenkins pipeline pushing images to DockerHub

Kubernetes deployment managed via GitHub

ArgoCD installed and application created

Auto-sync enabled:
Step 1 – Break the Running State

List running pods:
Step 1 – Break the Running State

List running pods:
kubectl get pods


Delete one pod manually to simulate failure:
kubectl delete pod flask-devops-deployment-6d594dfdfb-8n9w7


Step 2 – Watch Auto-Healing
kubectl get pods -w

Observed behavior:
| Status              | Meaning                        |
| ------------------- | ------------------------------ |
| `Terminating`       | Old pod deleted                |
| `Pending`           | Scheduler allocating resources |
| `ContainerCreating` | Pulling Docker image           |
| `Running`           | New pod successfully started   |



Step 3 – Git Drift Recovery

When incorrect image tag existed in Git:
image: awaismalak/flask-devops-app:v1



Pods went into:
ImagePullBackOff

Fix in Git:

image: awaismalak/flask-devops-app:28




Commit & push.

ArgoCD automatically detected the change and performed rolling update.

Final Result
| Component   | Status                                  |
| ----------- | --------------------------------------- |
| Jenkins     | Pushed new Docker image                 |
| GitHub      | Updated Kubernetes manifest             |
| ArgoCD      | Auto-synced new config                  |
| Kubernetes  | Terminated old pods & launched new ones |
| Application | Fully recovered with zero downtime      |


What I Learned

Git is the single source of truth

ArgoCD continuously monitors and reconciles drift

Kubernetes performs zero-downtime rolling updates

GitOps eliminates manual deployments






MALAK AWAIS




