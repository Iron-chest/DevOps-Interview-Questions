terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.0.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "3.0.0"
    }
  }
}

provider "local" {}
provider "tls" {}

# Resource to generate SSH key
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Resource to create cloud-config.yaml from the template
resource "local_file" "cloud_config" {
  filename = "${path.module}/cloud-config.yaml"
  content  = templatefile("${path.module}/cloud-config.yaml.tpl", {
    private_key = tls_private_key.ssh_key.private_key_pem
    public_key  = tls_private_key.ssh_key.public_key_pem
  })
}