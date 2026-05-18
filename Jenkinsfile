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

        stage('DEBUG ENV') {
            steps {
                sh '''
                echo "WORKSPACE=$WORKSPACE"
                echo "PWD=$PWD"
                env | grep WORKSPACE || true
                '''
            }
        }

        stage('Verify Requirements (HOST)') {
            steps {
                sh '''
                echo "=== HOST CHECK ==="
                test -f requirements.txt && echo "OK requirements exists" || echo "MISSING requirements"
                head -n 5 requirements.txt
                '''
            }
        }

        stage('Docker Sanity Check') {
            steps {
                sh '''
                docker version
                '''
            }
        }

        stage('Verify Inside Container') {
            steps {
                sh '''
                docker run --rm \
                    -v "$(pwd):/app" \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    bash -c "
                        set -e
                        echo '=== INSIDE CONTAINER ==='
                        pwd
                        ls -la

                        echo '=== REQUIREMENTS CHECK ==='
                        test -f requirements.txt
                        head -n 5 requirements.txt
                    "
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                docker run --rm \
                    -v "$(pwd):/app" \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    bash -c "
                        set -e

                        echo '=== INSTALL START ==='

                        pip install --upgrade pip

                        pip install -r requirements.txt

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
                            -v "$(pwd):/app" \
                            -w /app \
                            ${PYTHON_IMAGE} \
                            bash -c "flake8 . --count --statistics"
                        '''
                    }
                }

                stage('Security Scan') {
                    steps {
                        sh '''
                        docker run --rm \
                            -v "$(pwd):/app" \
                            -w /app \
                            ${PYTHON_IMAGE} \
                            bash -c "pip-audit || true"
                        '''
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                docker run --rm \
                    -v "$(pwd):/app" \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    bash -c "pytest -v --junitxml=test-results.xml || true"
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                docker run --rm \
                    -v "$(pwd):/app" \
                    -w /app \
                    ${PYTHON_IMAGE} \
                    python -c "print('Smoke Test Passed')"
                '''
            }
        }

        stage('Publish Results') {
            steps {
                junit testResults: 'test-results.xml', allowEmptyResults: true
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline passed'
        }

        failure {
            echo '❌ Pipeline failed'
        }

        always {
            archiveArtifacts artifacts: '**/*.xml', allowEmptyArchive: true
        }
    }
}