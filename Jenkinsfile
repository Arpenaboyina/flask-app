pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "arpenaboyina/flask-app-demo"   // ✅ Your Docker Hub repo
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS = "Rakesh"                 // ✅ Jenkins credentials ID (Docker Hub)
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/Arpenaboyina/flask-app.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          echo "🚀 Building Docker image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          // ✅ Windows uses 'bat' instead of 'sh'
          bat "docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} ."
        }
      }
    }

    stage('Smoke Test') {
      steps {
        script {
          echo "🧪 Running smoke tests..."

          // ✅ Remove any old test container if exists
          bat 'docker rm -f temp_test || exit 0'

          // ✅ Run new container
          bat "docker run -d --name temp_test -p 5000:5000 ${DOCKERHUB_REPO}:${IMAGE_TAG}"

          // ✅ Wait few seconds for startup (Windows ping)
          bat "ping -n 6 127.0.0.1 >nul"

          // ✅ Check app response (Windows PowerShell curl equivalent)
          bat 'powershell -Command "try { (Invoke-WebRequest -Uri http://localhost:5000/ -UseBasicParsing).StatusCode -eq 200 } catch { exit 1 }"'

          // ✅ Stop test container
          bat 'docker rm -f temp_test || exit 0'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          echo "📤 Pushing Docker image to Docker Hub..."

          // ✅ Login and push using Jenkins credentials
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
