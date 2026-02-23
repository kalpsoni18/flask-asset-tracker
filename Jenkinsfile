pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/kalpsoni18/flask-asset-tracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t asset-tracker:latest .'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 15'
                sh 'curl -f http://localhost:5000/health || exit 1'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful! App is live at port 5000.'
        }
        failure {
            echo '❌ Deployment failed. Check logs above.'
        }
    }
}
