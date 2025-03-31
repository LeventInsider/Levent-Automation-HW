pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
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

        stage('Setup Python') {
            steps {
                sh """
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    . ${VENV_PATH}/bin/activate
                    PYTHONPATH=$PYTHONPATH:$(pwd) pytest src/tests/test_insider_career.py \
                        --junitxml=test-results.xml \
                        --html=report.html \
                        -v
                """
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                junit 'test-results.xml'
            }
        }

        stage('Cleanup') {
            steps {
                cleanWs()
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
            echo 'Tests completed. Check the logs and screenshots for details.'
        }
    }
} 