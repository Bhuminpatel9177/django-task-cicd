pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'mydjangoapp:latest'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Bhuminpatel9177/django-task-cicd'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose run web python manage.py test'
            }
        }

        stage('Run Migrations') {
            steps {
                sh 'docker-compose run web python manage.py migrate'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up containers...'
            sh 'docker-compose down'
        }
    }
}
