pipeline {
    agent any
    
    stages {
        stage('Clone repository') {
            steps {
                // Remove existing directory if present
                deleteDir()
                
                // Clone the repository
                sh 'git clone https://github.com/MeghanaNamburu/Results-Chatbot.git'
            }
        }
        
        stage('Install dependencies') {
            steps {
                // Change directory to Results-Chatbot
                dir('Results-Chatbot') {
                    // Install dependencies
                    sh 'pip3 install -r requirements.txt'
                }
            }
        }
        
        stage('Run application') {
            steps {
                // Change directory to Results-Chatbot
                dir('Results-Chatbot') {
                    // Run the application
                    sh 'nohup python3 app.py &'
                }
            }
        }
    }
}

