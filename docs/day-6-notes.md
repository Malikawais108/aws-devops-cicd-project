# 📅 Day 6 – Kubernetes Ingress with NGINX

## 🎯 Objective

The goal of Day 6 was to expose our Flask application running inside Kubernetes to the outside world using **NGINX Ingress Controller** instead of NodePort or direct service access. This simulates real-world production traffic routing using host-based rules.

---

## 🏗️ Architecture Overview

User Browser / Client
↓ (HTTP request with Host header)
NGINX Ingress Controller (Minikube)
↓
Ingress Resource (Host-based rule)
↓
Kubernetes Service (ClusterIP)
↓
Flask Application Pods

---

## 🛠️ Prerequisites

* Minikube cluster running
* Jenkins pipeline already deploying application
* Flask app deployed with:

  * Deployment
  * Service (ClusterIP)
* NGINX Ingress Controller installed in cluster

Verification command:

```bash
kubectl get pods -n ingress-nginx
```

---

## 📂 Files Used (Kubernetes Directory)

```
kubernetes/
├── deployment.yaml
├── service.yaml
└── ingress.yaml   👈 (Created on Day 6)
```

---

## 🧾 Ingress Configuration (ingress.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-devops-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
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
```

### 🔑 Key Points

* `host` must match `/etc/hosts`
* `service.name` must match service.yaml
* `ingressClassName: nginx` binds ingress to NGINX controller

---

## 🚀 Apply Ingress

```bash
kubectl apply -f kubernetes/ingress.yaml
```

Verify:

```bash
kubectl get ingress
kubectl describe ingress flask-devops-ingress
```

---

## 🌐 DNS Mapping for Local Testing

Since this is a local Minikube setup, we map domain to Minikube IP.

Get Minikube IP:

```bash
minikube ip
```

Edit hosts file on local machine:

```bash
sudo vim /etc/hosts
```

Add:

```
192.168.58.2 flask-devops.local
```

---

## 🧪 Testing

### 1️⃣ Curl Test (Direct Ingress Validation)

```bash
curl -H "Host: flask-devops.local" http://192.168.58.2
```

✅ Output:

```json
{
  "environment": "production",
  "hostname": "flask-devops-deployment-xxxxx",
  "message": "CI/CD DevOps demo app running"
}
```

### 2️⃣ Browser Test

Open:

```
http://flask-devops.local
```

---

## ⚠️ Common Issues & Fixes

### ❌ Browser keeps loading

* Cause: `/etc/hosts` not mapped
* Fix: Map domain to Minikube IP

### ❌ Permission denied while editing files

* Cause: Using `sudo` as Jenkins user
* Fix: Edit files as normal user or change ownership

### ❌ Ingress created but not routing

* Cause: Missing ingressClassName
* Fix: Ensure `ingressClassName: nginx`

---

## 🎓 What I Learned (Interview Ready)

* Difference between **Service vs Ingress**
* How Ingress uses **Host headers**
* Why curl works with `-H Host` even if browser doesn’t
* Real-world traffic routing using NGINX
* Debugging Ingress using `describe` and logs

---

## ✅ Day 6 Completion Status

| Component                | Status       |
| ------------------------ | ------------ |
| NGINX Ingress Controller | ✅ Running    |
| Ingress Resource         | ✅ Working    |
| Service Routing          | ✅ Verified   |
| Browser Access           | ✅ Functional |

---

## ⏭️ Next Step

➡ **Day 7** – TLS / HTTPS with Ingress or Advanced CI/CD Enhancements
