pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p screenshots
                    python -m pytest src/tests/test_insider_career.py -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshots/*.png, report.html', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo "Tests completed successfully!"
        }
        failure {
            echo "Tests failed. Check the logs and screenshots for details."
        }
        always {
            echo "Cleaning up workspace..."
            cleanWs()
        }
    }
} 