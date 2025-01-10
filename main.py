import re
import json
import boto3
from pinecone import ServerlessSpec
from pinecone import Pinecone
pc = Pinecone(
    api_key="pcsk_2PqYLo_4z6FZVwzr9H3heXzps8m5MZcwsk6a5nvVveX6oh4axv8XSHXD1UY7Lq44v1k76o"
)
session = boto3.Session()
bedrock = boto3.client(service_name='bedrock-runtime', region_name = "us-east-1" )
modelId="amazon.titan-embed-text-v2:0"

index_name = "rubiesai"
index = pc.Index(index_name)



def embed(Question, Answer):
    """
    Chunking Strategy:
    1. Extract questions and answers from the text
    2. Ensure questions and answers are aligned
    3. Create chunks with questions and answers
    4. Return the chunks
    """

    # Prepare the input for the embedding model
    input_text = f"Q: {Question}\nA: {Answer}"

    # Create the input_data for the embedding request
    input_data = {
        "inputText": input_text,  # Embedding each chunk separately
        "dimensions": 1024,
        "normalize": True
    }

    # Serialize the data to JSON
    body = json.dumps(input_data).encode('utf-8')

    # Invoke Bedrock to get embeddings for this chunk
    response = bedrock.invoke_model(
        modelId=modelId,
        contentType="application/json",
        accept="*/*",
        body=body
    )

    response_body = response['body'].read()
    response_json = json.loads(response_body)

    # Extract the embedding for this chunk
    chunk_embedding = response_json['embedding']
    
    stats = index.describe_index_stats()
    print(stats)
    total_vectors = stats['total_vector_count']

    new_index = total_vectors 

    # Append the vector (ID, embedding, metadata)
    vectors = []
    vectors.append(
        (
            str(new_index),  # ID
            [chunk_embedding] if isinstance(chunk_embedding, float) else chunk_embedding,  # Vector
            {"question": Question, "answer": Answer}  # Metadata
        )
    )

    # Upsert vectors into the Pinecone index
    return index.upsert(vectors=vectors)

