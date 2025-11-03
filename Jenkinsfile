pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "arpenaboyina/flask-mysql-demo" // ✅ your Docker Hub repo
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds' // ✅ Jenkins credentials ID
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        script {
          echo "Building Docker image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
        }
      }
    }

    stage('Run Tests (smoke)') {
      steps {
        script {
          echo "Running smoke tests..."

          // Remove existing test container if any
          bat 'docker rm -f temp_test || exit 0'

          // Run the container
          def img = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
          img.run("-d --name temp_test -p 5000:5000")

          // Wait a few seconds for container to start
          bat "ping -n 6 127.0.0.1 >nul"

          // Check if Flask app responds
          bat '''
          curl --fail http://localhost:5000/ || (
            docker logs temp_test
            exit 1
          )
          '''

          // Cleanup
          bat 'docker rm -f temp_test || exit 0'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          echo "Pushing Docker image to Docker Hub..."

          docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
            def built = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
            built.push()
            built.push("latest")
          }
        }
      }
    }
  }

  post {
    always {
      echo "Cleaning up workspace..."
      bat 'docker rm -f temp_test || exit 0'
      cleanWs()
    }
    failure {
      mail to: 'arpenaboyina.rakesh@example.com',
           subject: "❌ Build failed: ${env.BUILD_URL}",
           body: "Build failed. Please check Jenkins logs for details."
    }
  }
}
