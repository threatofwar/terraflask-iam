from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print(f"FLASK_EXPOSE_HOST: {os.getenv('FLASK_EXPOSE_HOST')}")
print(f"FLASK_EXPOSE_PORT: {os.getenv('FLASK_EXPOSE_PORT')}")
