provider "aws" {
  region  = "ap-southeast-2"
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

resource "aws_iam_user" "user" {
  name = var.user_name
}

resource "aws_iam_policy_attachment" "policy_attach" {
  name       = "example-attachment"  # Provide a unique name
  users      = [aws_iam_user.user.name]  # Correct argument
  policy_arn  = var.policy
}
