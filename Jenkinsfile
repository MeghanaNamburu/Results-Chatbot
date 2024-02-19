pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository
                git branch: 'main', url: 'https://github.com/MeghanaNamburu/Results-Chatbot.git'
            }
        }
        stage('Run application') {
            steps {
                // Run the application
                sh 'nohup python3 app.py &'
            }
        }
    }
}
