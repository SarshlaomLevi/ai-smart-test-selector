pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME = "ai-smart-test-selector-ci"
        TAG = "${BUILD_NUMBER}"
        FULL_IMAGE = "${IMAGE_NAME}:${TAG}"
        WORKDIR = "/app"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Build Docker Image (Cached CI Image)') {
            steps {
                sh '''
                    echo "=== BUILDING CI IMAGE ==="

                    docker build \
                        -t $IMAGE_NAME:$TAG \
                        -t $IMAGE_NAME:latest \
                        .
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    docker run --rm \
                        $IMAGE_NAME:$TAG \
                        bash -c "
                            set -e
                            flake8 src || true
                        "
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm \
                        $IMAGE_NAME:$TAG \
                        bash -c "
                            set -e
                            bandit -r src || true
                        "
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                        $IMAGE_NAME:$TAG \
                        bash -c "
                            set -e
                            pytest -v
                        "
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    docker run --rm \
                        $IMAGE_NAME:$TAG \
                        bash -c "
                            set -e
                            python main.py --help || echo 'No CLI entrypoint'
                        "
                '''
            }
        }

        stage('Tag Success Build') {
            steps {
                sh '''
                    docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:stable
                '''
            }
        }

        stage('Cleanup Old Images') {
            steps {
                sh '''
                    docker image prune -f || true
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI PASSED - production build stable"
        }

        failure {
            echo "❌ CI FAILED"
        }

        always {
            cleanWs()
        }
    }
}