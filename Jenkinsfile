pipeline {
  agent any

  environment {
    IMAGE = "arpenaboyina/flask-app-demo"
    TAG = "${env.BUILD_NUMBER}"
    DOCKER_CREDENTIALS = "Rakesh"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${IMAGE}:${TAG} ./app"
        }
      }
    }

    stage('Smoke Test') {
      steps {
        script {
          sh "docker run -d --name temp_test -p 5001:5000 ${IMAGE}:${TAG}"
          sh "sleep 5"
          sh "curl -f http://localhost:5001/ || (docker logs temp_test && exit 1)"
        }
      }
      post {
        always {
          sh "docker rm -f temp_test || true"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
            sh "docker push ${IMAGE}:${TAG}"
            sh "docker tag ${IMAGE}:${TAG} ${IMAGE}:latest"
            sh "docker push ${IMAGE}:latest"
          }
        }
      }
    }
  }

  post {
    always {
      echo "Build finished: ${currentBuild.fullDisplayName}"
    }
  }
}

