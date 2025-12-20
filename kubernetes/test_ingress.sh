#!/bin/bash
IP=$(minikube ip)
echo "Testing HTTP..."
curl -H "Host: flask-devops.local" http://$IP
echo -e "\n\nTesting HTTPS..."
curl -k -H "Host: flask-devops.local" https://$IP

