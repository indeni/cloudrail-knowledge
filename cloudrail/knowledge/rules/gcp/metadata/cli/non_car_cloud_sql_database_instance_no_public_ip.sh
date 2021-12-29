# This will result in instance downtime

# First configure the instance to use a private IP
INSTANCE_ID=your_instance_id
PROJECT_ID=your_gcp_project_id
VPC_NETWORK_NAME=your_vpc_network_name

gcloud beta sql instances patch $INSTANCE_ID \
--project=$PROJECT_ID \
--network=projects/$PROJECT_ID/global/networks/$VPC_NETWORK_NAME \
--no-assign-ip

# Then disable the instance ipv4
gcloud sql instances patch $INSTANCE_ID \
--no-assign-ip

# and confirm it's disabled
gcloud sql instances describe $INSTANCE_ID
