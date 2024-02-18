pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository
                git branch: 'main', url: 'https://github.com/MeghanaNamburu/Results-Chatbot.git'
            }
        }
        stage('Install dependencies') {
            steps {
               script {
                    // Create a virtual environment
                    sh 'python3 -m venv venv'
                    // Activate the virtual environment and install dependencies
                    sh 'source venv/bin/activate && pip install -r Results-Chatbot/requirements.txt'
                }
            }
        }
        stage('Run application') {
            steps {
                // Run the application
                sh 'nohup python3 Results-Chatbot/app.py &'
            }
        }
    }
    post {
        always {
            // Deactivate the virtual environment after the pipeline completes
            sh 'deactivate'
        }
    }
}
