pipeline {
    agent {
        docker {
            image 'python:3.8'
        }
    }

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
                    # Check if Python is available
                    if command -v python3 &> /dev/null; then
                        python3 -m venv venv
                    elif command -v python &> /dev/null; then
                        python -m venv venv
                    else
                        echo "ERROR: Python not found. Please install Python 3.8 or later."
                        exit 1
                    fi
                    
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r levo_qa_automation/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    cd levo_qa_automation
                    mkdir -p screenshots
                    python3 -m pytest src/tests/test_insider_career.py -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'levo_qa_automation/test-results.xml'
                    archiveArtifacts artifacts: 'levo_qa_automation/screenshots/*.png, levo_qa_automation/report.html', allowEmptyArchive: true
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