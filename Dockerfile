# Base image for Python and Terraform
FROM python:3.11-slim

# Install Terraform
RUN apt-get update && \
    apt-get install -y curl unzip && \
    # Install Terraform
    curl -fsSL https://releases.hashicorp.com/terraform/1.5.5/terraform_1.5.5_linux_amd64.zip -o terraform.zip && \
    unzip terraform.zip -d /usr/local/bin && \
    rm terraform.zip && \
    # Install AWS CLI v2
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy Flask files
COPY flask/ /app/flask/

# Copy Terraform files
COPY terraform/ /app/terraform/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/flask/requirements.txt

# Expose Flask app port
EXPOSE 7000

# Command to run Flask by default
CMD ["python", "/app/flask/app.py"]
