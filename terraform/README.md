# terraform-aws-iam-user

git clone https://github.com/threatofwar/terraform-aws-iam-user.git
cd terraform-aws-iam-user
cp terraform.tfvars.example terraform.tfvars
```bash
aws_access_key_id     = "YOUR_AWS_ACCESS_KEY_ID"
aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY"
user_name             = "YOUR_IAM_USERNAME"
policy                = "YOUR_POLICY_ARN"
```
terraform init
terraform plan
terraform apply
terraform apply -auto-approve
