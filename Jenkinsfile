pipeline {
    /*
        prerequis:
        -  install postgresql, pipenv, pyenv
        -  Configure postgresql
    */
    agent any
    stages {
        stage("Launchin tests ...") {
            steps {
                sh "pipenv install"
                sh "pipenv run ./manage.py test substitutor.tests"
            }
        }
    }
}
