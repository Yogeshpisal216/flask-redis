pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "yogi2112"
        //IMAGE_NAME = "flask-backend"
        IMAGE_NAME = "flask-demo"
        IMAGE_TAG = "latest"
        K8S_NAMESPACE = "flask-redis"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG .
                    docker tag $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG $DOCKERHUB_USERNAME/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG
                    docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/redis-deployment.yaml
                    kubectl apply -f k8s/redis-service.yaml

                    sed -i "s|YOUR_DOCKERHUB_USERNAME/flask-redis-app:latest|$DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG|g" k8s/flask-blue-deployment.yaml

                    kubectl apply -f k8s/flask-blue-deployment.yaml
                    kubectl apply -f k8s/flask-service.yaml

                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    kubectl get pods -n $K8S_NAMESPACE
                    kubectl get svc -n $K8S_NAMESPACE
                '''
            }
        }
    }
}




