
resource "google_binary_authorization_policy" "policy" {
  default_admission_rule {
    evaluation_mode = "ALWAYS_DENY"
    enforcement_mode = "ENFORCED_BLOCK_AND_AUDIT_LOG"
  }

  cluster_admission_rules {
    cluster                 = "us-west1-a.gke-cluster-007"
    evaluation_mode         = "REQUIRE_ATTESTATION"
    enforcement_mode        = "ENFORCED_BLOCK_AND_AUDIT_LOG"
    require_attestations_by = [google_binary_authorization_attestor.attestor.name]
  }
}

resource "google_container_analysis_note" "note" {
  name = "test-attestor-note"
  attestation_authority {
    hint {
      human_readable_name = "My attestor"
    }
  }
}

resource "google_binary_authorization_attestor" "attestor" {
  name = "test-attestor"
  attestation_authority_note {
    note_reference = google_container_analysis_note.note.name
  }
}

resource "google_container_cluster" "cluster7" {
  name               = "gke-cluster-007"
  location           = "us-west1-a"
  initial_node_count = 3
  enable_binary_authorization = true
}
