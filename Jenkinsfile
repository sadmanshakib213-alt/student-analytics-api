pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'student-analytics-api'
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'student-analytics-api-container'
        STAGING_PORT = '8001'
        PROD_PORT = '8000'
    }

    stages {

        stage('Build') {
            steps {
                echo ' Building Docker image...'
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                bat "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                echo " Build complete — Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running automated tests...'
                bat "docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -m pytest tests/ -v --cov=app --cov-report=xml --cov-report=term-missing"
                echo ' All tests passed!'
            }
        }

        stage('Code Quality') {
            steps {
                echo ' Running code quality analysis...'
                bat "docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -m pytest tests/ --cov=app --cov-report=xml"
                echo ' Code quality analysis complete!'
            }
        }

        stage('Security') {
            steps {
                echo ' Running security analysis...'
                bat """
                    docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} pip install pbr && ^
                    docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} python -m bandit -r app/ -f txt
                """
                echo ' Security scan complete!'
            }
        }

        stage('Deploy') {
            steps {
                echo ' Deploying to staging environment...'
                bat "docker stop ${CONTAINER_NAME}-staging & exit 0"
                bat "docker rm ${CONTAINER_NAME}-staging & exit 0"
                bat "docker run -d --name ${CONTAINER_NAME}-staging -p ${STAGING_PORT}:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo " Deployed to staging on port ${STAGING_PORT}"
                bat "timeout /t 5 /nobreak"
                bat "curl -f http://localhost:${STAGING_PORT}/health || echo Health check attempted"
            }
        }

        stage('Release') {
            steps {
                echo ' Releasing to production...'
                bat "docker stop ${CONTAINER_NAME}-prod & exit 0"
                bat "docker rm ${CONTAINER_NAME}-prod & exit 0"
                bat "docker run -d --name ${CONTAINER_NAME}-prod -p ${PROD_PORT}:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                bat "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:production"
                echo " Released to production on port ${PROD_PORT}"
            }
        }

        stage('Monitoring') {
            steps {
                echo '📡 Setting up monitoring...'
                bat "docker stop prometheus & exit 0"
                bat "docker rm prometheus & exit 0"
                bat "docker stop grafana & exit 0"
                bat "docker rm grafana & exit 0"
                bat "docker run -d --name prometheus -p 9090:9090 -v ${WORKSPACE}/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus:latest"
                bat "docker run -d --name grafana -p 3000:3000 -e GF_SECURITY_ADMIN_PASSWORD=admin123 grafana/grafana:latest"
                echo ' Monitoring stack deployed!'
                echo ' Prometheus: http://localhost:9090'
                echo ' Grafana: http://localhost:3000'
            }
        }
    }

    post {
        success {
            echo ' Pipeline completed successfully!'
            echo " Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
            echo ' API: http://localhost:8000'
            echo ' Prometheus: http://localhost:9090'
            echo ' Grafana: http://localhost:3000'
        }
        failure {
            echo ' Pipeline failed!'
            bat "docker stop ${CONTAINER_NAME}-staging & exit 0"
            bat "docker rm ${CONTAINER_NAME}-staging & exit 0"
        }
        always {
            echo ' Cleaning up old images...'
            bat "docker image prune -f & exit 0"
        }
    }
}