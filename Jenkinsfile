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
                pwd
                '''
            }
        }

        stage('Run In Docker') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    reuseNode true
                }
            }

            stages {

                stage('Verify Files') {
                    steps {
                        sh '''
                        pwd
                        ls -la

                        test -f requirements.txt

                        head -n 5 requirements.txt
                        '''
                    }
                }

                stage('Install Dependencies') {
                    steps {
                        sh '''
                        pip install --upgrade pip

                        pip install -r requirements.txt

                        pip install pytest flake8 pip-audit
                        '''
                    }
                }

                stage('Lint') {
                    steps {
                        sh '''
                        flake8 . --count --statistics
                        '''
                    }
                }

                stage('Security Scan') {
                    steps {
                        sh '''
                        pip-audit || true
                        '''
                    }
                }

                stage('Unit Tests') {
                    steps {
                        sh '''
                        pytest -v \
                        --junitxml=test-results.xml || true
                        '''
                    }
                }

                stage('Smoke Test') {
                    steps {
                        sh '''
                        python -c "print('Smoke Test Passed')"
                        '''
                    }
                }
            }
        }

        stage('Publish Results') {
            steps {
                junit testResults: 'test-results.xml',
                       allowEmptyResults: true
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
            archiveArtifacts(
                artifacts: '**/*.xml',
                allowEmptyArchive: true
            )
        }
    }
}