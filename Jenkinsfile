pipeline {
    agent any

    environment {
        API_URL = "http://localhost:8000"
    }

    stages {

        // =====================================================
        // 1. CHECKOUT SOURCE CODE
        // =====================================================
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        // =====================================================
        // 2. SETUP PYTHON ENVIRONMENT
        // =====================================================
        stage('Install Dependencies') {
            steps {
                sh '''
                docker run --rm -v $WORKSPACE:/app -w /app python:3.11-slim \
                bash -c "pip install --upgrade pip && pip install -r requirements.txt"
                '''
            }
        }
        // =====================================================
        // 3. START FASTAPI SERVICE
        // =====================================================
        stage('Start API Server') {
            steps {
                sh '''
                . venv/bin/activate
                nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
                sleep 10
                '''
            }
        }

        // =====================================================
        // 4. FETCH CRITICAL TESTS FROM API
        // =====================================================
        stage('Fetch Critical Tests') {
            steps {
                script {
                    def response = sh(
                        script: "curl -s ${env.API_URL}/critical-tests",
                        returnStdout: true
                    ).trim()

                    echo "Critical Tests Response: ${response}"

                    writeFile file: 'critical_tests.json', text: response
                }
            }
        }

        // =====================================================
        // 5. EXECUTE ONLY CRITICAL TESTS
        // =====================================================
        stage('Run Critical Tests') {
            steps {
                script {

                    def tests = readJSON file: 'critical_tests.json'

                    if (tests.size() == 0) {
                        echo "No critical tests found. Skipping execution."
                        return
                    }

                    for (test in tests) {

                        echo "Running test: ${test.test_name}"

                        // Hook for your real test framework execution
                        sh """
                        echo "Executing ${test.test_name}"
                        python run_test.py --name ${test.test_name}
                        """
                    }
                }
            }
        }

        // =====================================================
        // 6. QUALITY GATE (FAIL BUILD IF RISK IS TOO HIGH)
        // =====================================================
        stage('Quality Gate') {
            steps {
                script {

                    def tests = readJSON file: 'critical_tests.json'

                    def criticalCount = 0

                    for (test in tests) {

                        if (test.failure_probability > 0.85) {
                            criticalCount++
                        }
                    }

                    echo "Number of critical high-risk tests: ${criticalCount}"

                    if (criticalCount > 2) {
                        error("❌ Build failed due to too many high-risk tests")
                    } else {
                        echo "✅ Build passed quality gate successfully"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed"
        }
    }
}