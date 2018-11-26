// -*- groovy -*-

pipeline {
  agent any

  environment {
    PYTEST_ADDOPTS = '--color=yes'
  }

  stages {
    stage('Test') {
      steps {
        timeout(15) {
          ansiColor('xterm') {
            sh './backend/run_tests.sh'
          }
        }
      }
    }
  }

  post {
    always {
      junit healthScaleFactor: 200.0,           \
        testResults: '**/build/reports/*.xml'

      cobertura coberturaReportFile: 'backend/coverage.xml',    \
        maxNumberOfBuilds: 0

      cleanWs()
    }
  }
}
