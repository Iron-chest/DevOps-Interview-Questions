# AWS EC2 Instance Configuration with SSH Keys using Terraform

## Project Description
This project automates the creation of SSH keys and generates a `cloud-config.yaml` file for an EC2 instance using Terraform 0.14.5. The solution uses the `tls` and `local` providers to generate RSA 4096-bit keys and render a configuration file based on a provided template.

## Prerequisites
Before you begin, ensure you have the following software installed on your machine:

### Required Software
1. **Terraform 0.14.5**
   - Download from [Terraform Downloads](https://releases.hashicorp.com/terraform/0.14.5/).
   - Install Terraform by following the [installation guide](https://learn.hashicorp.com/tutorials/terraform/install-cli).

2. **AWS CLI (optional for testing)**
   - Install via [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

3. **Text Editor**
   - Any code editor (e.g., Visual Studio Code, Sublime Text, or Vim).

4. **Git**
   - Install via [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Initialize Terraform Providers**
   Initialize the project to download required providers.
   ```bash
   terraform init
   ```

3. **Validate the Configuration**
   Ensure the Terraform configuration is correct.
   ```bash
   terraform validate
   ```

4. **Plan the Execution**
   Review the planned actions before applying.
   ```bash
   terraform plan
   ```

5. **Apply the Configuration**
   Execute the plan to generate SSH keys and the `cloud-config.yaml` file.
   ```bash
   terraform apply
   ```

6. **Verify Output**
   The `cloud-config.yaml` file and SSH keys will be generated in the specified paths.

## Project Structure
```
.
├── main.tf                # Main Terraform configuration file
├── cloud-config.yaml.tpl  # Template for cloud-config.yaml
├── variables.tf           # Input variables definition
├── outputs.tf             # Output configuration
└── README.md              # Documentation
```

## main.tf
```hcl
terraform {
  required_version = "0.14.5"
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

resource "tls_private_key" "ssh_keys" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "cloud_config" {
  content  = templatefile("cloud-config.yaml.tpl", {
    private_key = tls_private_key.ssh_keys.private_key_pem
    public_key  = tls_private_key.ssh_keys.public_key_openssh
  })
  filename = "cloud-config.yaml"
}

output "private_key" {
  value = tls_private_key.ssh_keys.private_key_pem
}

output "public_key" {
  value = tls_private_key.ssh_keys.public_key_openssh
}
```

## cloud-config.yaml.tpl
```yaml
write_files:
    - path: /etc/app/key
      permissions: '0600'
      content: |
        ${private_key}
    - path: /etc/app/key.pub
      permissions: '0644'
      content: |
        ${public_key}
```

## variables.tf
Define additional input variables here if required.

## outputs.tf
Capture and display the generated keys.

```hcl
output "private_key" {
  description = "Generated private key."
  value       = tls_private_key.ssh_keys.private_key_pem
}

output "public_key" {
  description = "Generated public key."
  value       = tls_private_key.ssh_keys.public_key_openssh
}
```

## Usage
- Customize the `cloud-config.yaml.tpl` template as needed.
- Integrate the generated keys and configuration file into your AWS EC2 instance deployment pipeline.

## Troubleshooting
1. **Provider Installation Issues**: Ensure the required provider versions are specified correctly in `main.tf`.
2. **Template Rendering Errors**: Check for syntax issues in `cloud-config.yaml.tpl` and ensure placeholders match.
3. **Validation Errors**: Use `terraform validate` to identify configuration issues.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
