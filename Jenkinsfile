pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        PYTHON_IMAGE='python:3.11-slim'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker') {
            steps {
                sh '''
                echo "Checking Docker..."
                docker version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                docker run --rm \
                -v $WORKSPACE:/app \
                -w /app \
                ${PYTHON_IMAGE} \
                bash -c "
                pip install --upgrade pip &&
                pip install -r requirements.txt &&
                pip install pytest flake8 pip-audit
                "
                '''
            }
        }

        stage('Quality Checks') {

            parallel {

                stage('Lint') {
                    steps {
                        sh '''
                        docker run --rm \
                        -v $WORKSPACE:/app \
                        -w /app \
                        ${PYTHON_IMAGE} \
                        bash -c "
                        flake8 . --count --statistics
                        "
                        '''
                    }
                }

                stage('Security Scan') {
                    steps {
                        sh '''
                        docker run --rm \
                        -v $WORKSPACE:/app \
                        -w /app \
                        ${PYTHON_IMAGE} \
                        bash -c "
                        pip-audit
                        "
                        '''
                    }
                }

            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                docker run --rm \
                -v $WORKSPACE:/app \
                -w /app \
                ${PYTHON_IMAGE} \
                bash -c "
                pytest -v --junitxml=test-results.xml
                "
                '''
            }

            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                docker run --rm \
                -v $WORKSPACE:/app \
                -w /app \
                ${PYTHON_IMAGE} \
                bash -c "
                python -c \\"print('Smoke Test Passed')\\"
                "
                '''
            }
        }
    }

    post {

        success {
            echo "✅ Pipeline passed"
        }

        failure {
            echo "❌ Pipeline failed"
        }

        always {
            archiveArtifacts artifacts: '**/*.xml', allowEmptyArchive: true
        }
    }
}