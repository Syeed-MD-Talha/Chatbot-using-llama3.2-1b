import chromadb
import pprint

# Initialize the Chroma client
client = chromadb.PersistentClient(path="/db/")

# Delete the existing collection if it exists
try:
    client.delete_collection(name="db1")
    print("Deleted existing collection 'db1'.")
except Exception as e:
    print(f"Collection 'db1' does not exist or could not be deleted: {e}")

# Create a new collection
database = client.create_collection(name="db1")

# Add documents to the collection
database.add(
    ids=["doc1", "doc2", "doc3", "doc4", "doc5", "doc6"],
    metadatas=[{"topic": "programming"}, {"topic": "animal"}, {"topic": "animal"},
               {"topic": "animal"}, {"topic": "human"}, {"topic": "news"}],
    documents=[
        "A programming language is a set of instructions and rules that allows humans to communicate with computers to create software applications. It provides a way to write programs that tell a computer what to do, such as processing data, performing calculations, or controlling hardware. Programming languages can be broadly categorized into low-level languages, which are closer to machine code, and high-level languages, which are easier for humans to read and write. Popular high-level programming languages include Python, Java, and C++, each with its own strengths and use cases. Programming languages are used in various fields, including web development, data analysis, artificial intelligence, and mobile app development. Learning a programming language helps individuals solve problems, automate tasks, and build innovative solutions.",
        "This is a document about animal's food",
        "This is a document about cats",
        "This is a document about dogs",
        "This is a document about human",
        "This is a document about news"
    ]
)

# Query the collection
results = database.query(
    n_results=1,
    query_texts=["tell me about programming"], 
)

# Print the results
pprint.pprint(results)

result = results["documents"][0][0]
print(result)

import requests

# Define the URL of the Ollama API
url = "http://127.0.0.1:11434/api/generate"

# Define the payload (input data) for the API request
payload = {
    "model": "llama3.2:1b",  # Use the correct model name
    "prompt": f"summarize this text:{result} within 20 words",  # Your input prompt
    "stream": False  # Set to True if you want streaming responses
}

# Send a POST request to the Ollama API
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()
    
    # Extract only the response text
    answer = result.get("response", "No response found.")
    print("\nResponse from Ollama:", answer)
else:
    print(f"Failed to get a response. Status code: {response.status_code}")
    print("Response content:", response.text)