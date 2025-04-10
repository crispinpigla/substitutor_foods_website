pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh "./manage.py test substitutor.tests"
            }
        }
    }
}
