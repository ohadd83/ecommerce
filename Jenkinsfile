pipeline {

    agent any

    environment {

        // Docker Hub repository
        IMAGE_NAME = "ohadd306/python-ecommerce-api"

        // Docker container name
        CONTAINER_NAME = "python-ecommerce-api"

        // Application port on EC2
        APP_PORT = "8000"

        // Jenkins build number becomes the image version
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {


        stage('Test') {

            steps {

                echo "Running Python tests..."

                sh '''
                    python3 -m pytest -v
                '''
            }
        }


// build docker image

        stage('Build Docker Image') {

            steps {

                echo "Building Docker image..."

                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        .
                '''
            }
        }


//test docker image

        stage('Test Docker Image') {

            steps {

                echo "Starting temporary test container..."

                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME}-test \
                        -p 8001:8000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''

                echo "Waiting for application..."

                sleep 5

                echo "Running health check..."

                sh '''
                    curl -f http://localhost:8001/health
                '''
            }

            post {

                always {

                    echo "Removing test container..."

                    sh '''
                        docker rm -f ${CONTAINER_NAME}-test || true
                    '''
                }
            }
        }


// push docker image

        stage('Push to Docker Hub') {

            steps {

                echo "Logging into Docker Hub..."

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASSWORD" | \
                        docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker push \
                            ${IMAGE_NAME}:${IMAGE_TAG}

                        docker logout
                    '''
                }
            }
        }


//  deploy application

        stage('Deploy') {

            steps {

                echo "Deploying application..."

                sh '''
                    docker stop ${CONTAINER_NAME} || true

                    docker rm ${CONTAINER_NAME} || true

                    docker pull \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:8000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

// production healthcheck 

        stage('Health Check') {

            steps {

                echo "Checking production application..."

                sleep 5

                sh '''
                    curl -f \
                        http://localhost:${APP_PORT}/health
                '''
            }
        }
    }


// pipeline result 

    post {

        success {

            echo """
            ==========================================
              DEPLOYMENT SUCCESSFUL
            ==========================================

            Application:
            ${IMAGE_NAME}:${IMAGE_TAG}

            Container:
            ${CONTAINER_NAME}

            Port:
            ${APP_PORT}

            ==========================================
            """
        }

        failure {

            echo """
            ==========================================
              PIPELINE FAILED
            ==========================================
            """
        }
    }
}
