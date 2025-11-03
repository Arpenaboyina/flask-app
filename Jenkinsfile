pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "arpenaboyina/flask-app-demo"   // ✅ your Docker Hub repo
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS = "Rakesh"                 // ✅ your Jenkins credentials ID
  }

  stages {
    stage('Checkout') {
      steps {
        // ✅ Works only if Pipeline type is "Pipeline script from SCM"
        checkout scm
        // (If you are pasting manually instead, use:
        // git branch: 'main', url: 'https://github.com/Arpenaboyina/flask-app.git')
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          echo "🚀 Building Docker image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          // ✅ Build from current workspace
          bat "docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} ."
        }
      }
    }

    stage('Smoke Test') {
      steps {
        script {
          echo "🧪 Running smoke tests..."

          // Remove any old test container if exists
          bat 'docker rm -f temp_test || exit 0'

          // Run new container
          bat "docker run -d --name temp_test -p 5000:5000 ${DOCKERHUB_REPO}:${IMAGE_TAG}"

          // Wait few seconds for startup
          bat "ping -n 6 127.0.0.1 >nul"

          // Check response
          bat 'curl --fail http://localhost:5000/ || (docker logs temp_test && exit 1)'

          // Stop test container
          bat 'docker rm -f temp_test || exit 0'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          echo "📤 Pushing Docker image to Docker Hub..."

          // ✅ Login & push using credentials
          docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
            def img = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
            img.push()
            img.push("latest")
          }
        }
      }
    }
  }

  post {
    always {
      echo "🧹 Cleaning up workspace..."
      bat 'docker rm -f temp_test || exit 0'
      cleanWs()
    }

    failure {
      echo "❌ Build failed. Please check logs."
    }
  }
}
