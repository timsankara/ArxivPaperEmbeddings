from flask import Flask, request, jsonify
import json
import boto3
from botocore.exceptions import NoCredentialsError
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from arxiv_api import ArxivAPI  # Import the ArxivAPI class from the package


# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
load_dotenv()
config = dotenv_values(".env")

client = OpenAI(api_key=config['OPENAI_API_KEY'])
# Initialize DynamoDB client with AWS credentials from environment variables
ACCESS_KEY = config['AWS_ACCESS_KEY_ID']
SECRET_KEY = config['AWS_SECRET_ACCESS_KEY']

# Initialize DynamoDB client with AWS credentials
dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='us-east-1' # change to preffered region
)

# Define the name of the DynamoDB table
TABLE_NAME = ''  # Change to your DynamoDB table name

# Function to save embeddings to DynamoDB
def save_to_dynamodb(embeddings):
    try:
        # Put embeddings into DynamoDB table
        dynamodb_client.put_item(
            TableName=TABLE_NAME,
            Item={
                'embedding_id': {'S': embeddings['id']},
                'embedding_data': {'S': json.dumps(embeddings)}
            }
        )
        return True
    except NoCredentialsError:
        return False  # Return False if authentication fails
    except Exception as e:
        return False

@app.route('/get-arxiv-papers', methods=['GET'])
def get_arxiv_papers():
    try:
        category = "cs.AI" # change to preffered category
        max_results = 10 # change to required number of papers

        # If max_results is not provided, set a default value
        if max_results is None:
            max_results = 10  # Default value
        else:
            max_results = int(max_results)  # Convert max_results to an integer

        # Create an instance of the ArxivAPI class with the specified parameters
        arxiv_api = ArxivAPI(category, max_results)

        # Fetch, parse, and retrieve papers
        data = arxiv_api.fetch_data()
        papers = arxiv_api.parse_data(data)

        # Return the papers as JSON response
        return jsonify({'papers': papers})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to create embedding from body
@app.route('/create-embedding-from-body', methods=['POST'])
def create_embedding_from_body():
    try:
        body = request.get_json()

        embeddings = client.embeddings.create(input = [body['input']], model='text-embedding-ada-002').data[0].embedding

        # Save embeddings to DynamoDB
        save_to_dynamodb(embeddings)

        return jsonify({'message': 'Embeddings saved to DynamoDB successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)