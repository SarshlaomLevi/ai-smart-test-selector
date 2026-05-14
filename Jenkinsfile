pipeline {
    agent none

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        PYTHON_IMAGE = 'python:3.11-slim'
        PIP_CACHE_DIR = '/tmp/pip-cache'
    }

    stages {

        // =====================================================
        // 1. Checkout
        // =====================================================
        stage('Checkout') {
            agent any
            steps {
                checkout scm
            }
        }

        // =====================================================
        // 2. Install Dependencies (Docker-based)
        // =====================================================
        stage('Install Dependencies') {
            agent {
                docker {
                    image "${PYTHON_IMAGE}"
                    reuseNode true
                }
            }

            steps {
                sh """
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        // =====================================================
        // 3. Lint (Quality Gate #1)
        // =====================================================
        stage('Lint') {
            agent {
                docker {
                    image "${PYTHON_IMAGE}"
                    reuseNode true
                }
            }

            steps {
                sh """
                    pip install flake8
                    flake8 . --count --show-source --statistics
                """
            }
        }

        // =====================================================
        // 4. Unit Tests
        // =====================================================
        stage('Unit Tests') {
            agent {
                docker {
                    image "${PYTHON_IMAGE}"
                    reuseNode true
                }
            }

            steps {
                sh """
                    pip install pytest
                    pytest -v --junitxml=test-results.xml
                """
            }

            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        // =====================================================
        // 5. Run Application Smoke Test
        // =====================================================
        stage('Smoke Test API') {
            agent {
                docker {
                    image "${PYTHON_IMAGE}"
                    reuseNode true
                }
            }

            steps {
                sh """
                    python -m pip install -r requirements.txt
                    python -c "print('Smoke test placeholder - start API here')"
                """
            }
        }

        // =====================================================
        // 6. Security / Dependency Check (optional but pro)
        // =====================================================
        stage('Security Scan') {
            agent {
                docker {
                    image "${PYTHON_IMAGE}"
                    reuseNode true
                }
            }

            steps {
                sh """
                    pip install pip-audit
                    pip-audit || true
                """
            }
        }
    }

    // =====================================================
    // Post Actions (NVIDIA-style observability)
    // =====================================================
    post {
        success {
            echo "✅ Pipeline passed successfully"
        }

        failure {
            echo "❌ Pipeline failed - check logs"
        }

        always {
            archiveArtifacts artifacts: '**/*.log, **/*.xml', allowEmptyArchive: true
        }
    }
}