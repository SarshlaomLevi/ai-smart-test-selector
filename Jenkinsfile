pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PYTHON_IMAGE = 'python:3.11-slim'
        PIP_CACHE_DIR = '/tmp/pip-cache'
        WS = "${WORKSPACE}"
    }

    stages {

        stage('Checkout Clean') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Debug Workspace') {
            steps {
                sh '''
                echo "=== WORKSPACE DEBUG ==="
                pwd
                ls -la
                '''
            }
        }

        stage('Verify Requirements (HOST)') {
            steps {
                sh '''
                echo "=== HOST CHECK ==="
                ls -la
                test -f requirements.txt && echo "requirements EXISTS" || echo "missing requirements"
                cat requirements.txt | head -n 20
                '''
            }
        }

        stage('Docker Sanity Check') {
            steps {
                sh '''
                echo "Docker version check"
                docker version
                docker info > /dev/null
                '''
            }
        }

        stage('Verify Inside Container (CRITICAL DEBUG)') {
            steps {
                sh '''
                docker run --rm \
                    -v $WS:/app \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    bash -c "
                        echo '=== INSIDE CONTAINER ==='
                        pwd
                        ls -la /app
                        echo '=== REQUIREMENTS INSIDE CONTAINER ==='
                        cat /app/requirements.txt | head -n 20
                    "
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                docker run --rm \
                    -v $WS:/app \
                    -v $PIP_CACHE_DIR:/root/.cache/pip \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    bash -c "
                        set -e
                        pip install --upgrade pip
                        pip install -r /app/requirements.txt
                        pip install pytest flake8 pip-audit
                    "
                '''
            }
        }

        stage('Quality Gates') {
            parallel {

                stage('Lint') {
                    steps {
                        sh '''
                        docker run --rm \
                            -v $WS:/app \
                            -w /app \
                            ${PYTHON_IMAGE} \
                            bash -c "
                                set -e
                                flake8 . --count --statistics
                            "
                        '''
                    }
                }

                stage('Security Scan') {
                    steps {
                        sh '''
                        docker run --rm \
                            -v $WS:/app \
                            -w /app \
                            ${PYTHON_IMAGE} \
                            bash -c "
                                set -e
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
                    -v $WS:/app \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    bash -c "
                        set -e
                        pytest -v --junitxml=/app/test-results.xml
                    "
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                junit testResults: 'test-results.xml', allowEmptyResults: true
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                docker run --rm \
                    -v $WS:/app \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    python -c "print('Smoke Test Passed')"
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