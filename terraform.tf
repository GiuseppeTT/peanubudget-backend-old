terraform {
  required_version = "~> 1.3"

  cloud {
    organization = "giutt-org"
    workspaces {
      name = "peanubudget-workspace"
    }
  }
}
