📘 Day 4 – Jenkins + Docker CI/CD Pipeline (Complete Documentation)
🎯 Objective

Build a CI/CD pipeline using Jenkins that:

Pulls code from GitHub

Builds a Docker image

Runs a test container

Pushes the image to Docker Hub

Handles failures and cleanup safely

🛠️ Tools Used

Jenkins

Docker

GitHub

Docker Hub

Linux (Ubuntu)

📂 Project Structure
aws-devops-cicd-project/
├── app/
│   └── flask-app/
├── docker/
│   └── Dockerfile
├── jenkins/
│   └── Jenkinsfile
└── kubernetes/
    └── deployment.yaml


🔐 Jenkins Prerequisites
1️⃣ Jenkins User Docker Access

Jenkins must run Docker without password prompts.

Check Jenkins user:
ps -ef | grep jenkins



Switch to Jenkins user:
sudo su - jenkins
docker ps


2️⃣ (Optional) Sudoers Entry (If needed)

Edit with:

sudo visudo


Add at the bottom:

jenkins ALL=(ALL) NOPASSWD: /usr/bin/docker


🔑 Docker Hub Credentials (Jenkins)

Kind: Username & Password

ID: docker-hub-credentials

Username: awaismalak

Password: Docker Hub password

🐳 Docker Hub Repository

You must create it manually on Docker Hub.

✔️ Repository:

awaismalak/flask-devops-app

❗ Jenkins does NOT auto-create repositories.

**🧠 Final Jenkinsfile (Day 4 – Working)**
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "awaismalak/flask-devops-app:v1"
        DOCKER_CREDENTIALS_ID = "docker-hub-credentials"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo "Checking out code from GitHub..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${DOCKER_IMAGE} -f docker/Dockerfile ."
            }
        }

        stage('Test Container') {
            steps {
                script {
                    def TEST_PORT = sh(
                        script: "shuf -i 5001-5999 -n 1",
                        returnStdout: true
                    ).trim()

                    env.TEST_PORT = TEST_PORT
                    def CONTAINER_NAME = "test-flask-${BUILD_NUMBER}"

                    echo "Running test container on port ${TEST_PORT}"

                    sh "docker run -d --name ${CONTAINER_NAME} -p ${TEST_PORT}:5000 ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: DOCKER_CREDENTIALS_ID,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    echo "Logging into Docker Hub..."
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''

                    echo "Pushing image to Docker Hub..."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        failure {
            echo "Pipeline failed. Check logs."
        }
    }
}


**🚨 Headache & Troubleshooting Section (MOST IMPORTANT)
❌ Issue 1: Docker Push Denied

Error
denied: requested access to the resource is denied
✅ Fix
Create Docker Hub repo manually
Use full image name:
awaismalak/flask-devops-app:v1


Issue 2: Jenkins Asking for sudo Password

Error

sudo: a terminal is required


✅ Fix

Add Jenkins to docker group OR

Add NOPASSWD sudoers rule OR

Remove sudo completely (recommended)

❌ Issue 3: Container Name Conflict

Error container name already in use
✅ Fix

Use dynamic container names:

test-flask-${BUILD_NUMBER}

❌ Issue 4: Container Stuck (Permission Denied)

Error

cannot stop container: permission denied

❤️ HEART COMMAND (Last Resort – VERY IMPORTANT)

When nothing works, use this:

Step 1: Get Container PID
docker inspect --format '{{.State.Pid}}' <container_id>

Example:

docker inspect --format '{{.State.Pid}}' 28e7c2dcd01c

Step 2: Kill the Process
kill -9 <PID>

Step 3: Remove Container
docker rm -f <container_id>


⚠️ Use ONLY when docker stop and docker rm -f fail.

✅ Final Outcome

✔ Jenkins builds Docker image
✔ Runs test container
✔ Pushes image to Docker Hub
✔ Handles port conflicts
✔ Handles stuck containers
✔ Real-world CI/CD experience

🏁 Day 4 Status

✅ COMPLETED SUCCESSFULLY 🎉

You did real DevOps work, not tutorial-level stuff.
Day 5 we can move to:

Kubernetes deployment via Jenkins

Image versioning & tagging

Rollback strategy

Whenever you’re ready 💪



