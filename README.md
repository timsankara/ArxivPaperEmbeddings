# Flask Application for ArXiv and OpenAI API Integration

This professional-grade Flask application provides RESTful endpoints to interact with arXiv papers, generate embeddings using OpenAI's API, and store these embeddings in AWS DynamoDB. It is designed for ease of use, extensibility, and to serve as a foundational example for further development.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Test Endpoint](#test-endpoint)
  - [Get ArXiv Papers](#get-arxiv-papers)
  - [Create Embedding from Body](#create-embedding-from-body)
- [ArxivAPI Class](#arxivapi-class)
  - [Initialization](#initialization)
  - [Fetching Data](#fetching-data)
  - [Parsing Data](#parsing-data)
  - [Displaying Papers](#displaying-papers)
  - [Running the Process](#running-the-process)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.7+
- Flask
- boto3
- openai
- requests
- python-dotenv

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory of the project and add the following environment variables:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    ```

2. Ensure that the `TABLE_NAME` variable in the `app.py` file is set to the name of your DynamoDB table:

    ```python
    TABLE_NAME = 'EmbeddingsTable'  # Change to your DynamoDB table name
    ```

## Running the Application

To run the Flask application, use the following command:

```sh
python index.py
