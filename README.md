# <p align="center">Breaking-Builds</p>


<p align="center">
  <img src="https://github.com/saad-out/Breaking-Builds/blob/main/walter.png" style="width:300px;"/>
</p>

# <p align="center">Real time full CI/CD pipeline with Jenkins. </p>



## Overview

*Breaking-Builds* is a full CI/CD pipeline demo showcasing the journey of code from development to production, with each stage powered by Jenkins. The pipeline automates builds, tests, and deployments, ensuring that every line of code goes through the rigorous process of "cooking"—just like Heisenberg's meticulous lab work. This project demonstrates the power of automation in software delivery while having a fun Breaking Bad theme!

With this project, you can trigger builds, watch the stages unfold, and see firsthand how code is tested and deployed—without worrying about the DEA catching up with you.

## Features

- **Automated Builds**: The pipeline automatically builds code whenever a change is detected.
- **Automated Testing**: Unit tests are executed during the pipeline to ensure high-quality code.
- **Deployment**: Code is deployed automatically to production upon successful testing.
- **Real-time Updates**: Track the progress of each stage in the pipeline with live feedback.
- **Integration with GitHub**: GitHub integration ensures that every commit triggers the CI/CD pipeline.

## Tech Stack

- **Jenkins**: Orchestrates the entire CI/CD pipeline.
- **GitHub**: Hosts the code repository.
- **Python**: Used for backend code and tests.
- **Render**: Hosts the backend API.
- **Docker**: Used for containerized environments in Jenkins.
- **React**: Frontend for viewing build logs live and interacting with the pipeline interface.
- **Github pages**: Hosts the **React** frontend.

## Workflow

The Breaking-Builds pipeline follows a continuous integration and deployment process, orchestrated through Jenkins and triggered by both GitHub webhooks and the web app itself.

### Backend (Flask API)

The backend, built with Flask, connects to Jenkins via its API, enabling actions such as triggering builds and retrieving build information. It serves as a bridge between the frontend and Jenkins, providing endpoints to initiate builds and fetch real-time updates on the build stages and logs.

### Frontend (React)

The frontend, built with React, allows users to view the build logs and see the progress of each pipeline stage live. Users trigger builds manually through the web interface, simulating the pipeline for a more interactive experience. Each stage is displayed hierarchically, showing detailed logs as the build progresses.
Jenkins Pipeline

The Jenkins pipeline, defined in a `Jenkinsfile`, is configured to automate builds, testing, and deployments. It is triggered in two main ways:

1. **Webhook Trigger**: When new changes are pushed to GitHub, a webhook triggers the pipeline. For changes pushed to the `dev` branch, the pipeline merges to `main` after successful testing, which automatically redeploys the API (hosted on Render) in production.

2. **Manual Trigger via Web App**: Users can trigger a build through the web app interface, which simulates the workflow, providing a mock deployment to allow users to experience the CI/CD process.

### Pipeline Stages Explained

1. **Setup**: Initializes the environment, setting the branch name for reference in later stages.
2. **Build**: Installs necessary dependencies for the backend API.
3. **Test**: Runs unit tests to validate code quality.
4. **Deploy - Mock**: For non-dev branches, performs a mock deployment to simulate the CI/CD process.
5. **Deploy - Production**: For the `dev` branch, merges changes to `main` to trigger deployment on Render.

### Jenkins Configuration

The Jenkins setup for Breaking-Builds is configured to support Docker-based build agents and a custom pipeline. Below are key configuration details:

#### 1. **Jenkins Master**

The Jenkins master is hosted on a cloud server, configured specifically for personal use. It controls the CI/CD pipeline by orchestrating Docker agents that run the build, test, and deployment stages. The master instance connects securely to GitHub for source code management.

#### 2. **Docker Agent**

The pipeline relies on Docker agents configured with the label `docker-python`. The agent image `devopsjourney1/myjenkinsagents:python` is used, which is pre-configured with Python to support backend builds and testing. The Docker agent runs each stage in an isolated environment, ensuring dependencies are correctly installed and reducing potential conflicts.

#### 3. **SSH Credentials**

Jenkins requires SSH credentials to authenticate with GitHub and deploy to production. A Jenkins credential, labeled `JK`, is used for secure authentication during the production deployment stage. This enables Jenkins to merge changes from the `dev` branch into `main` and push updates automatically.

#### 4. **Jenkinsfile and Branch Management**

The Jenkinsfile defines the pipeline stages and logic. Specific configurations include:

- **Branch Detection**: The `BRANCH_NAME` environment variable is set based on the branch being built, which affects deployment behavior.
- **Build Triggers**: Builds are triggered by GitHub webhooks for `dev` branch changes, leading to automatic deployment to main for production.
- **API Integration:** Builds can also be triggered manually via the web app, simulating the CI/CD process.
