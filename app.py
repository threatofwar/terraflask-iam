from flask import Flask, request, jsonify
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()

app = Flask(__name__)

def user_exists(username):
    """Check if the IAM user exists."""
    try:
        subprocess.run(['aws', 'iam', 'get-user', '--user-name', username], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@app.route('/provision', methods=['POST'])
def provision():
    data = request.json
    username = data.get('username')
    policy = data.get('policy')

    terraform_dir = os.getenv('TERRAFORM_DIR')
    tfvars_file = f'{terraform_dir}/terraform.tfvars'

    existing_vars = {}
    if os.path.exists(tfvars_file):
        with open(tfvars_file, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.split('=')
                    existing_vars[key.strip()] = value.strip().strip('"')

    with open(tfvars_file, 'a') as f:
        if 'user_name' not in existing_vars:
            f.write(f"\nuser_name = \"{username}\"\n")
        if 'policy' not in existing_vars:
            f.write(f"policy = \"{policy}\"\n")

    if user_exists(username):
        print(f"User {username} exists.")
        print(f"Importing existing IAM user: {username}")
        try:
            subprocess.run(['terraform', 'import', f'aws_iam_user.user', username], check=True, cwd=terraform_dir)
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'failure', 'message': str(e)}), 500

    try:
        subprocess.run(['terraform', 'init'], check=True, cwd=terraform_dir)
        subprocess.run(['terraform', 'apply', '-auto-approve', '-var-file=terraform.tfvars'], check=True, cwd=terraform_dir)
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_EXPOSE_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_EXPOSE_PORT', 8000)))