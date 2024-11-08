pipeline {
    agent {
        node {
            label 'docker-python'
        }
    }
    triggers {
        pollSCM('*/5 * * * *')
    }
    stages {
        stage('Build') {
            steps {
                echo "Building... for branch ${env.BRANCH_NAME}"
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
                sh '''
                cd app/backend
                source venv/bin/activate
                python3 -m unittest discover
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploying... for branch ${env.BRANCH_NAME}"
                sh '''
                cd app/backend
                source venv/bin/activate
	            echo "Mock deploy"
                '''
            }
        }
    }
}
