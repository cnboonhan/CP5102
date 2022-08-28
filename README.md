# CP5102

### Local Infrastructure Setup
```
# Keep ports 8080 and 5432 free
# Install AWSCLIv2, Docker, Docker-Compose, Terraform, postgresql-client-14
pip3 install terraform-local
pip3 install checkov

# Configure AWS
mkdir -p ~/.aws && cp -r aws-credentials/* ~/.aws

# set in bashrc for convenience
complete -C '/usr/local/bin/aws_completer' aws
alias aws="aws --endpoint-url=http://localhost:4566"
```

### Provisioning Example Vulnerable Infrastructure
```
cd terraform/[dir]

# Deploy
tflocal init 
tflocal apply --auto-approve

# View bucket
aws s3api list-buckets
```

### Connecting to psql database
```
psql --host 127.0.0.1 -U postgres
```

### Scanning
```
checkov --directory terraform/[dir]
```
