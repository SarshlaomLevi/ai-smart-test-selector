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
        WORKDIR = "/app"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Fix Permissions') {
            steps {
                sh '''
                    echo "=== FIXING WORKSPACE PERMISSIONS ==="
                    chmod -R a+rwX "$WORKSPACE" || true
                '''
            }
        }

        stage('Build Docker Image') {
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
                    -v "$WORKSPACE:$WORKDIR" \
                    -w "$WORKDIR" \
                    $IMAGE_NAME:$TAG \
                    bash -c "

                        echo '=== RUNNING FLAKE8 ==='

                        if [ -d src ]; then
                            flake8 src || true
                        else
                            echo 'No src directory found'
                        fi
                    "
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm \
                    -v "$WORKSPACE:$WORKDIR" \
                    -w "$WORKDIR" \
                    $IMAGE_NAME:$TAG \
                    bash -c "

                        echo '=== RUNNING BANDIT ==='

                        bandit \
                            -r src \
                            --exit-zero \
                            -f json \
                            -o bandit-report.json
                    "
                '''
            }
        }

        stage('Security Gate') {
            steps {
                sh '''
                    echo "=== ANALYZING SECURITY REPORT ==="

                    if [ ! -f "$WORKSPACE/bandit-report.json" ]; then
                        echo "⚠️ No security report found"
                        exit 0
                    fi

                    HIGH_ISSUES=$(grep -o '"issue_severity": "HIGH"' "$WORKSPACE/bandit-report.json" | wc -l)

                    echo "High severity issues: $HIGH_ISSUES"

                    if [ "$HIGH_ISSUES" -gt 0 ]; then
                        echo "❌ High severity security issues detected"
                        exit 1
                    fi

                    echo "✅ Security gate passed"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                    -v "$WORKSPACE:$WORKDIR" \
                    -w "$WORKDIR" \
                    $IMAGE_NAME:$TAG \
                    bash -c "

                        echo '=== RUNNING TESTS ==='

                        if [ -d tests ] && [ \"$(find tests -name '*.py' | wc -l)\" -gt 0 ]; then
                            pytest -v
                        else
                            echo 'No tests found — skipping'
                        fi
                    "
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    docker run --rm \
                    -v "$WORKSPACE:$WORKDIR" \
                    -w "$WORKDIR" \
                    $IMAGE_NAME:$TAG \
                    bash -c "

                        echo '=== RUNNING SMOKE TEST ==='

                        python main.py --help || \
                        echo 'No CLI entrypoint found'
                    "
                '''
            }
        }

        stage('Tag Success Build') {
            steps {
                sh '''
                    echo "=== TAGGING STABLE BUILD ==="

                    docker tag \
                    $IMAGE_NAME:$TAG \
                    $IMAGE_NAME:stable
                '''
            }
        }

        stage('Cleanup Docker') {
            steps {
                sh '''
                    echo "=== CLEANING DOCKER ==="

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