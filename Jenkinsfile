pipeline {
    agent {
        node {
            label 'docker-python'
        }
    }
    stages {
        stage ('Setup')
        {
            steps {
                script {
                        // Set default branch to main, if it's not set
                        env.BRANCH_NAME = "${GIT_BRANCH.split("/")[1]}"
                    }
            }
        }
        stage('Build') {
            steps {
                echo "Building... for branch ${env.BRANCH_NAME}"
                // Install dependencies
                sh '''
                cd app/backend
                python3 -m venv venv
                source venv/bin/activate
	            pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing... for branch ${env.BRANCH_NAME}"
                // Run tests
                sh '''
                cd app/backend
                source venv/bin/activate
                python3 -m unittest discover
                '''
            }
        }
        stage('Deploy - Mock')
        {
            // Mock Deployment for non-dev branches (for testing purposes)
            when {
                expression {
                    return env.BRANCH_NAME != 'dev'
                }
            }
            steps {
                echo "Deploying... for branch ${env.BRANCH_NAME}"
                // Deploy to mock environment
                sh '''
                cd app/backend
                source venv/bin/activate
                echo "Deploying to mock environment"
                '''
            }
        }
        stage('Deploy - Production')
        {
            // Deploy to production for dev branche
            when {
                expression {
                    return env.BRANCH_NAME == 'dev'
                }
            }
            steps {
                sshagent (['jk']) {
                    echo "Deploying... for branch ${env.BRANCH_NAME}"
                    // Deploy to production environment
                    // API hosted on Render, merge dev to main will automatically deploy to production
                    sh '''
                    git checkout main
                    git pull origin main
                    git merge origin/dev
                    git push origin main
                    '''
                }
            }
        }
    }
}
