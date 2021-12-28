
DATABASE_INSTANCE_NAME=your_instance_name
gcloud sql instances patch $DATABASE_INSTANCE_NAME --database-flags "cross db ownership chaining=off"
