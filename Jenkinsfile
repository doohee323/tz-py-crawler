pipeline {
   agent any

   environment {
     // You must set the following environment variables in Jenkins configuration
     // ORGANIZATION_NAME
     // YOUR_DOCKERHUB_USERNAME (it doesn't matter if you don't have one)

     GIT_BRANCH = "master"
     SERVICE_NAME = "tz-py-crawler"
     REPOSITORY_TAG="${YOUR_DOCKERHUB_USERNAME}/${ORGANIZATION_NAME}-${SERVICE_NAME}:${BUILD_ID}"
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
            sh '''ls'''
         }
      }

      stage('Build and Push Image') {
         steps {
           sh 'docker image build -t ${REPOSITORY_TAG} .',
           sh 'docker push ${REPOSITORY_TAG}'
         }
      }

      stage('Deploy to Cluster') {
          steps {
            sh 'envsubst < ${WORKSPACE}/tz-py-crawler.yaml | kubectl apply -f -'
          }
      }
   }
}
