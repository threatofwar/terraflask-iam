variable "aws_access_key_id" {
    description = "AWS access key"
}

variable "aws_secret_access_key" {
    description = "AWS secret access key"
}

variable "user_name" {
    description = "The name of the IAM user"
}

variable "policy" {
    description = "The ARN of the IAM policy to attach"
}