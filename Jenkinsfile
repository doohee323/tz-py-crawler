pipeline {
   agent any

   environment {
     // You must set the following environment variables in Jenkins configuration
     // ORGANIZATION_NAME
     // YOUR_DOCKERHUB_USERNAME (it doesn't matter if you don't have one)

     GIT_BRANCH = "master"
     DOCKER_VERSION = "latest"
     SERVICE_NAME = "tz-py-crawler"
     REPOSITORY_TAG="${YOUR_DOCKERHUB_USERNAME}/${SERVICE_NAME}:${DOCKER_VERSION}"

     registry = "doohee323/tz-py-crawler"
     // Add a Credentials for dockerhub
     // http://98.234.161.130:31000/credentials/
     // ex) Jenkins	(global)	dockerhub	doohee323/****** (dockerhub)
     registryCredential = 'dockerhub'
     dockerImage = ''
   }

   stages {
      stage('Preparation') {
         steps {
            cleanWs()
            git credentialsId: 'GitHub',
            url: "https://github.com/${ORGANIZATION_NAME}/${SERVICE_NAME}",
            branch: "${GIT_BRANCH}"
         }
      }
      stage('Build') {
         steps {
            script {
                dockerImage = docker.build registry + ":$BUILD_NUMBER"
            }
//            sh 'docker image build -t ${REPOSITORY_TAG} .'
         }
      }

      stage('Push Image') {
         steps {
            script {
                docker.withRegistry( '', registryCredential ) {
                    dockerImage.push()
                }
            }
//            sh 'docker push ${REPOSITORY_TAG}'
         }
      }

      stage('Cleaning up') {
        steps{
            sh "docker rmi $registry:$BUILD_NUMBER"
        }
      }

      stage('Deploy to Cluster') {
          steps {
            sh 'envsubst < ${WORKSPACE}/tz-py-crawler.yaml | kubectl apply -f -'
          }
      }
   }
}
