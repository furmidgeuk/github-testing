terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.9.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = ">= 2.22.0"
    }
  }
}

variable "environment" {
  description = "Deployment environment (dev, test, val, prd)"
  type        = string
}

variable "location" {
  description = "Azure region for the resource group"
  type        = string
  default     = "UK South"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.environment}"
  location = var.location
}
