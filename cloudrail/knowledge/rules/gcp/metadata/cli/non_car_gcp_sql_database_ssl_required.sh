INSTANCE_NAME=your_cloudsql_instance_name
gcloud sql instances patch $INSTANCE_NAME --require-ssl
