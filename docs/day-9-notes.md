Jenkins – DockerHub – GitHub – ArgoCD GitOps CI/CD Pipeline
🔹 Architecture Flow
Developer Push → Jenkins
Jenkins → Build Docker Image
Jenkins → Push Image to DockerHub
Jenkins → Update Kubernetes Manifest in GitHub
GitHub → ArgoCD Detects Change → Auto Deploy to K8s

🔹 Required Tools
Tool	Purpose
Jenkins	CI pipeline
Docker	Image build
DockerHub	Image registry
GitHub	GitOps repo
Kubernetes	Deployment cluster
ArgoCD	GitOps CD
🔹 Jenkins Credentials
1️⃣ DockerHub Credentials
Field	Value
Kind	Username with password
ID	docker-hub-credentials
Username	awaismalak
Password	DockerHub password
2️⃣ GitHub Token Credentials

GitHub → Settings → Developer Settings → Tokens → Classic Token

Permissions:

✔ repo
✔ workflow


Jenkins Credential:

Field	Value
Kind	Username with password
ID	github-token
Username	your GitHub username
Password	GitHub PAT
🔹 Jenkinsfile (FINAL)
pipeline {
    agent any

    environment {
        IMAGE_NAME = "awaismalak/flask-devops-app"
        DOCKER_CREDS = credentials('docker-hub-credentials')
        GIT_CREDS = credentials('github-token')
        GIT_REPO = "https://github.com/Malikawais108/aws-devops-cicd-project.git"
        BRANCH = "main"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${BRANCH}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -f docker/Dockerfile .'
            }
        }

        stage('DockerHub Login') {
            steps {
                sh 'echo ${DOCKER_CREDS_PSW} | docker login -u ${DOCKER_CREDS_USR} --password-stdin'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push ${IMAGE_NAME}:${BUILD_NUMBER}'
            }
        }

        stage('Update Kubernetes Manifest') {
            steps {
                sh '''
                sed -i "s|image: .*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g" kubernetes/deployment.yaml
                git config user.email "ci@jenkins.com"
                git config user.name "Jenkins CI"
                git add kubernetes/deployment.yaml
                git commit -m "Update image tag to ${BUILD_NUMBER}"
                git push https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@github.com/Malikawais108/aws-devops-cicd-project.git ${BRANCH}
                '''
            }
        }
    }
}

🔹 ArgoCD Port Forward

If 8080 already used by Jenkins:

kubectl port-forward svc/argocd-server -n argocd 9090:443


Access:

https://localhost:9090

🔹 Verify Deployment
kubectl get pods
kubectl describe pod <pod-name>

🛑 Troubleshooting
Error	Reason	Fix
could not read Username for 'https://github.com'	No GitHub token	Add GitHub PAT in Jenkins
Couldn't find any revision to build	Branch mismatch (master vs main)	Use branch main everywhere
permission denied /var/run/docker.sock	Jenkins user no Docker permission	sudo usermod -aG docker jenkins && sudo systemctl restart jenkins
sed: can't read kubernetes/deployment.yaml	Wrong path	Confirm file location
port-forward 8080 already in use	Jenkins using 8080	Use 9090
Image not updating in cluster	ArgoCD not synced	Refresh & Sync in ArgoCD
🏆 Result

Every Jenkins build now:

✔ Builds Docker image
✔ Pushes to DockerHub
✔ Updates GitHub manifest
✔ ArgoCD auto deploys to Kubernetes


#---> MALAK AWAIS
