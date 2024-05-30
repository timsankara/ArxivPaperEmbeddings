from flask import Flask, request, jsonify
import json
import boto3
from botocore.exceptions import NoCredentialsError
import openai
import os
from arxiv_api import ArxivAPI  # Import the ArxivAPI class from the package


# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize DynamoDB client with AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize DynamoDB client with AWS credentials
dynamodb = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Define the name of the DynamoDB table
TABLE_NAME = 'EmbeddingsTable'  # Change to your DynamoDB table name


# Function to save embeddings to DynamoDB
def save_to_dynamodb(embeddings):
    try:
        # Put embeddings into DynamoDB table
        response = dynamodb.put_item(
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
        print(e)
        return False

@app.route('/', methods=['GET'])
def test():
    return "Hello World!"

@app.route('/get-arxiv-papers', methods=['GET'])
def get_arxiv_papers():
    try:
        category = "cs.AI"
        max_results = 10

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
        data = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=body['input']
        )
        # Save embeddings to DynamoDB
        if save_to_dynamodb(data):
            return jsonify({'message': 'Embeddings saved to DynamoDB successfully'})
        else:
            return jsonify({'error': 'Failed to save embeddings to DynamoDB. Authentication error.'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)