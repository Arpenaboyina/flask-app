pipeline {
  agent any

  environment {
    // ✅ Your Docker Hub repo name
    DOCKERHUB_REPO = "arpenaboyina/flask-app-demo"

    // ✅ Use Jenkins build number as tag for versioning
    IMAGE_TAG = "${env.BUILD_NUMBER}"

    // ✅ Jenkins credentials ID for Docker Hub login (you added it as 'Rakesh')
    DOCKERHUB_CREDENTIALS = 'Rakesh'
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

    stage('Build Image') {
      steps {
        script {
          echo "🐳 Building Docker image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
        }
      }
    }

    stage('Run Tests (smoke)') {
      steps {
        script {
          echo "🧪 Running smoke tests on the Flask container..."

          // Remove old test container if exists
          bat 'docker rm -f temp_test || exit 0'

          // Run new test container with environment variables
          def img = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
          img.run("-d --name temp_test -p 5000:5000 ^
            -e MYSQL_HOST=db ^
            -e MYSQL_USER=myuser ^
            -e MYSQL_PASSWORD=mypassword ^
            -e MYSQL_DATABASE=mydb")

          // Wait a few seconds for Flask to boot
          bat "ping -n 8 127.0.0.1 >nul"

          // Test app response
          bat '''
            echo Checking Flask endpoint...
            curl --fail http://localhost:5000/ || (
              echo ❌ Flask test failed. Printing container logs...
              docker logs temp_test
              exit 1
            )
          '''

          // Cleanup container
          bat 'docker rm -f temp_test || exit 0'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          echo "📤 Pushing Docker image to Docker Hub..."
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
      echo "🧹 Cleaning up workspace and containers..."
      bat 'docker rm -f temp_test || exit 0'
      cleanWs()
    }
    success {
      echo "✅ CI/CD pipeline completed successfully for build #${env.BUILD_NUMBER}!"
    }
    failure {
      echo "❌ Build failed. Check console logs for details."
      mail to: 'rakesh@iiitdwd.ac.in',
           subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
           body: """
Hello Rakesh,

The Jenkins CI/CD build for your Flask + MySQL project has failed.
Check the Jenkins console output for more details:

${env.BUILD_URL}

Regards,
Jenkins CI/CD Bot
"""
    }
  }
}
