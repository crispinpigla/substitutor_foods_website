pipeline {
    /*
        prerequis:
        -  install postgresql, pipenv, pyenv, vi (or nano), firefox (https://support.mozilla.org/fr/kb/installer-firefox-linux#w_install-firefox-deb-package-for-debian-based-distributions)
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
