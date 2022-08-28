# CP5102

```
# Install AWSCLIv2, Docker, Docker-Compose
aws configure --profile default

AWS_ACCESS_KEY_ID="test"
AWS_SECRET_ACCESS_KEY="test"
AWS_DEFAULT_REGION="ap-southeast-1"

# set in bashrc for convenience
complete -C '/usr/local/bin/aws_completer' aws
alias aws="aws --endpoint-url=http://localhost:4566"
```
