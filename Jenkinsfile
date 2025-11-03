pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = "arpenaboyina/flask-app-demo"    // Your Docker Hub repo
        IMAGE_TAG = "latest"
        DOCKERHUB_CREDENTIALS = "Rakesh"                  // Jenkins credentials ID for Docker Hub
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Cloning repository from GitHub...'
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/Arpenaboyina/flask-app.git']]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                bat '''
                    echo Building Docker image for Flask app...
                    docker build -t arpenaboyina/flask-app-demo:latest .
                '''
            }
        }

        stage('Test Container') {
            steps {
                echo '🧪 Running test container...'
                bat '''
                    echo Running test container...
                    docker run -d --name test-flask -p 5000:5000 arpenaboyina/flask-app-demo:latest

                    echo Waiting for Flask app to start...
                    powershell -Command "Start-Sleep -Seconds 10"

                    echo Testing the Flask app endpoint...
                    curl -f http://localhost:5000 || (docker logs test-flask & exit 1)

                    echo Stopping and removing test container...
                    docker stop test-flask
                    docker rm test-flask
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Logging in and pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}",
                                                 usernameVariable: 'USER',
                                                 passwordVariable: 'PASS')]) {
                    bat '''
                        echo %PASS% | docker login -u %USER% --password-stdin
                        docker push arpenaboyina/flask-app-demo:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                echo '🚀 Deploying new container on port 5000...'
                bat '''
                    echo Checking for existing container on port 5000...

                    for /f "tokens=*" %%i in ('docker ps -a -q --filter "publish=5000"') do (
                        echo Stopping container using port 5000...
                        docker stop %%i
                        docker rm %%i
                    )

                    echo Checking for existing flask-app container...
                    for /f "tokens=*" %%j in ('docker ps -a -q --filter "name=flask-app"') do (
                        echo Stopping existing flask-app container...
                        docker stop %%j
                        docker rm %%j
                    )

                    echo Starting new container on port 5000...
                    docker run -d --name flask-app -p 5000:5000 arpenaboyina/flask-app-demo:latest
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up unused Docker resources...'
                bat 'docker image prune -f'
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD pipeline completed successfully!'
        }
        failure {
            echo '❌ Build failed. Check the console output for details.'
        }
    }
}
