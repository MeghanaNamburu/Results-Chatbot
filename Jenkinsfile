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
                // Install dependencies
                sh 'pip3 install -r Results-Chatbot/requirements.txt'
            }
        }
        stage('Run application') {
            steps {
                // Run the application
                sh 'nohup python3 Results-Chatbot/app.py &'
            }
        }
    }
}
