#!/usr/bin/env bash

# build and deploy the cloud run api
# how to run
# sh deploy_cloud_run.sh PROJECT_ID SERVICE_NAME IMAGE_NAME IMAGE_TAG
# e.g.
# sh deploy_cloud_run.sh ml-console-dev slammer slammer 0.0.1
# sh deploy_cloud_run.sh social-media-ingestion slammer slammer 0.0.2


PROJECT_ID=$1
SERVICE_NAME=$2
IMAGE_NAME=$3
IMAGE_TAG=$4


region=us-central1


PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG .
if [ $? -ne 0 ]
then
    echo "Error building docker image. Exiting"
    exit 1;
else
    echo "Pushing docker image"
    docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG
fi

#gcloud builds submit --tag gcr.io/$project_id/$image_name

#service_account=$service_account@$PROJECT_ID.iam.gserviceaccount.com
service_account=$PROJECT_NUMBER-compute@developer.gserviceaccount.com


gcloud beta run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG \
  --project $PROJECT_ID \
  --region $region \
  --platform managed \
  --cpu 2 \
  --memory 2Gi \
  --concurrency 100 \
  --timeout 3600 \
  --allow-unauthenticated \
  --service-account $service_account
