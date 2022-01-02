resource "google_project" "my_project" {
  name       = "My Project"
  project_id = "your-project-id"
  labels = {
    "environment" = "test",
    "Name" = "project-my"
  }
}