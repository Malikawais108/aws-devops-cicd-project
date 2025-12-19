Day 5: Jenkins CI/CD with Docker & Kubernetes
Overview

On Day 5, we connected Jenkins with Kubernetes to achieve a full CI/CD pipeline for our Flask application:

Jenkins builds the Docker image.

Jenkins runs a test container to verify the image.

Jenkins pushes the image to Docker Hub.

Jenkins deploys the updated image to Kubernetes.

Cleanup is performed.

1. Jenkins User Kubernetes Setup

Problem:
kubectl get pods as Jenkins user failed due to permission issues with .kube and .minikube.

Solution Steps:
# Create .kube folder for Jenkins
sudo mkdir -p /var/lib/jenkins/.kube

# Copy your user's kubeconfig to Jenkins
sudo cp ~/.kube/config /var/lib/jenkins/.kube/config

# Give ownership to Jenkins user
sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube

# Fix permissions for Minikube certificates
sudo chmod -R g+rX /home/malakawais/.minikube
sudo chmod -R o+rX /home/malakawais/.minikube

Tip:
Replace paths in config to point to the proper .minikube certificates accessible by Jenkins if needed.

2. Jenkins Pipeline (Jenkinsfile)

Jenkinsfile structure for Day 5:
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "awaismalak/flask-devops-app:v1"
        DOCKER_CREDENTIALS_ID = "docker-hub-credentials"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "Checking out code from Git..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${DOCKER_IMAGE}..."
                sh "docker build -t ${DOCKER_IMAGE} -f docker/Dockerfile ."
            }
        }

        stage('Test Container') {
            steps {
                script {
                    def TEST_PORT = sh(script: "shuf -i 5001-5999 -n 1", returnStdout: true).trim()
                    env.TEST_PORT = TEST_PORT
                    echo "Running test container on port ${TEST_PORT}"
                    sh "docker rm -f test-flask-devops-app || true"
                    sh "docker run -d --name test-flask-devops-app -p ${TEST_PORT}:5000 ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDENTIALS_ID}", 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS')]) {
                    
                    echo "Logging in to Docker Hub..."
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    echo "Pushing Docker image ${DOCKER_IMAGE}..."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                sh "sed -i 's|image: awaismalak/flask-devops-app:.*|image: ${DOCKER_IMAGE}|g' kubernetes/deployment.yaml"
                sh "kubectl apply -f kubernetes/deployment.yaml"
                sh "kubectl apply -f kubernetes/service.yaml"
                sh "kubectl rollout status deployment/flask-app"
            }
        }

        stage('Cleanup Test Container') {
            steps {
                echo "Cleaning up test container..."
                sh "docker rm -f test-flask-devops-app || true"
            }
        }
    }

    post {
        always { echo "Pipeline finished!" }
        failure { echo "Pipeline failed! Check logs." }
    }
}


3. Kubernetes Deployment & Service YAML
   Deployment (kubernetes/deployment.yaml)

   apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: awaismalak/flask-devops-app:v1
        ports:
        - containerPort: 5000


Service (kubernetes/service.yaml)

apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: NodePort


4. Common Commands

Check pods:

kubectl get pods -A
kubectl get pods
kubectl get svc


View rollout status:
kubectl rollout status deployment/flask-app


Delete a container manually if needed:

docker ps -a
docker rm -f <container_id>
docker inspect --format '{{.State.Pid}}' <container_id>
kill -9 <pid>

Check minikube status:
minikube status

5. Troubleshooting

Permission issues for Jenkins user:
Error: unable to read client-cert /home/malakawais/.minikube/profiles/minikube/client.crt

Fix:
sudo chmod -R g+rX /home/malakawais/.minikube
sudo chmod -R o+rX /home/malakawais/.minikube

Cleanup test container fails:
cannot remove container "test-flask-devops-app": permission denied

Fix:

Add Jenkins to Docker group:
sudo usermod -aG docker jenkins

Or run cleanup step with sudo in pipeline.

Minikube status fails for Jenkins user:

Ensure .minikube files are readable by Jenkins.

Sometimes it’s easier to restart Jenkins after permission fixes.

6. Pipeline Outcome

Docker image successfully pushed: awaismalak/flask-devops-app:v1-21.

Kubernetes deployment updated and rolled out successfully.

Jenkins pipeline status: SUCCESS ✅


Auther:
Malak Awais
