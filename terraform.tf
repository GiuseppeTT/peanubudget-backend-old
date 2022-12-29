terraform {
  required_version = "~> 1.3"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.33"
    }

    random = {
      source  = "hashicorp/random"
      version = "~>3.4"
    }
  }

  cloud {
    organization = "giutt-org"
    workspaces {
      name = "app-budget-terraform-cloud-workspace"
    }
  }
}

provider "azurerm" {
  features {}
}
