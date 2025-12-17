# Day 1 – Project Initialization & Planning

## Date
17 Dec 2025

## Objectives
- Initialize DevOps CI/CD project repository
- Define clean project structure
- Set up Git and push to GitHub
- Prepare placeholders for future implementation

## Tasks Completed
- Created main project directory `aws-devops-cicd-project`
- Defined standard DevOps folder structure:
  - app (application code)
  - docker (Dockerfile)
  - jenkins (Jenkinsfile)
  - terraform (IaC modules)
  - kubernetes (manifests)
  - monitoring (Prometheus & Grafana)
- Added `.gitkeep` files to track empty directories
- Created `README.md` with project overview
- Initialized Git repository
- Committed initial structure
- Pushed project to GitHub (main branch)

## Key Learnings
- Git does not track empty directories
- `.gitkeep` is used to preserve folder structure
- Avoid using sudo for project files to prevent permission issues
- Importance of incremental commits in DevOps projects

## Challenges Faced
- File permission issues due to sudo usage
- Resolved by changing ownership using `chown`

## Next Steps (Day 2)
- Create Flask application
- Write Dockerfile
- Build and run Docker container locally

