from flask import Flask, request, jsonify
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()

app = Flask(__name__)

@app.route('/provision', methods=['POST'])
def provision():
    data = request.json
    username = data.get('username')
    policy = data.get('policy')

    # Place terraform project directory
    terraform_dir = os.getenv('TERRAFORM_DIR')
    
    tfvars_content = f"""
    user_name = "{username}"
    policy = "{policy}"
    """
    with open(f'{terraform_dir}/terraflask.tfvars', 'w') as f:
        f.write(tfvars_content)

    # Exec Terraform commands
    try:
        subprocess.run(['terraform', 'init'], check=True, cwd=terraform_dir)
        subprocess.run(['terraform', 'apply', '-auto-approve', '-var-file=terraflask.tfvars'], check=True, cwd=terraform_dir)
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError:
        return jsonify({'status': 'failure'}), 500

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_EXPOSE_HOST','0.0.0.0'), port=int(os.getenv('FLASK_EXPOSE_PORT',8000)))

