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
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "=== BUILDING IMAGE ==="

                    docker build \
                    -t $IMAGE_NAME:$TAG \
                    -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    docker run --rm \
                    $IMAGE_NAME:$TAG \
                    bash -c "
                        echo '=== RUNNING FLAKE8 ==='
                        flake8 src
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
                        echo '=== RUNNING BANDIT ==='

                        bandit \
                        -r src \
                        --exit-zero \
                        -f json \
                        -o /tmp/bandit-report.json
                    "
                '''
            }
        }

        stage('Unit Tests + Coverage') {
            steps {
                sh '''
                    docker run --rm \
                    -e PYTHONPATH=/app/src \
                    $IMAGE_NAME:$TAG \
                    bash -c "
                        echo '=== RUNNING TESTS ==='
                        pytest tests -v --cov=src --cov-report=term
                    "
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    docker run --rm \
                    -e PYTHONPATH=/app/src \
                    $IMAGE_NAME:$TAG \
                    bash -c "
                        echo '=== RUNNING SMOKE TEST ==='
                        python src/ai_smart_test_selector/main.py --help
                    "
                '''
            }
        }

        stage('Tag Stable') {
            steps {
                sh '''
                    docker tag \
                    $IMAGE_NAME:$TAG \
                    $IMAGE_NAME:stable
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    docker image prune -f || true
                '''
            }
        }
    }

    post {

        success {
            echo "✅ CI PASSED"
        }

        failure {
            echo "❌ CI FAILED"
        }

        always {
            cleanWs()
        }
    }
}
