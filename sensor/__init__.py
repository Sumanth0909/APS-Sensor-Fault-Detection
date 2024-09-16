#  To make sure that our "environment variables" (the variables which are there inside ".env" file) 
# are accessible everywhere else too, we have to write a code as follows

from dotenv import load_dotenv
print(f"Loading environment variable from .env file")
load_dotenv()