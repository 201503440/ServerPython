pipeline {
  agent any  
  stages {

    stage('Git') {
      steps {
        git branch: 'main', url: 'https://github.com/201503440/ServerPython'
      }
    }

    stage('Build image') {
      steps { sh 'sudo docker build -t pythonimage src/' }
    }    
    
    stage('Create container') {
      steps { sh 'sudo docker run -d -p 5000:5000 pythonimage' }
    }    
    
  }
}