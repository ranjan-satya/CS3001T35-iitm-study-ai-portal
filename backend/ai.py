import openai
import json
import os

# Set your API key here
api_key =  os.getenv('OPENAI_API_KEY')


# Initialize the OpenAI client
openai.api_key = api_key

def get_ai_response(question, query, option_selected):
    # Create a prompt that includes the question, query, and option selected by the user
    prompt = (
        f"Question: {question}\n"
        f"Query: {query}\n"
        f"Option selected by user: {option_selected}\n\n"
        "Provide the following in JSON format:\n"
        "{\n"
        "  \"answer\": \"<the answer to the question>\",\n"
        "  \"explanation\": \"<a detailed explanation of why this option is the best choice in the context of the query>\"\n"
        "}\n"
        "Ensure that the JSON is properly formatted and valid and there is no error in the code."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Using the gpt-3.5-turbo model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,  # Adjust the response length if needed
        temperature=0.7  # Adjust the creativity level of the response
    )
    
    # Extract and parse the response text
    response_text = response.choices[0].message['content'].strip()
    if response_text.startswith('```'):
        response_text =  response_text[7:-3]
    try:
        response_dict = json.loads(response_text)
    except json.JSONDecodeError:
        response_dict = {"error": "Failed to parse response as JSON", "raw_response": response_text}
    
    return response_dict

def get_ai_response_code(question, query, code):
    # Create a prompt that includes the question, query, and option selected by the user
    prompt = (
        f"Question: {question}\n"
        f"Query: {query}\n"
        f"code given by user: {code}\n\n"
        "Provide the following in JSON format:\n"
        "{\n"
        "  \"answer\": \"<the correct code answer to the question>\",\n"
        "  \"explanation\": \"<a detailed explanation of why this code is the best choice in the context of the query>\"\n"
        "}\n"
        "Ensure that the JSON is properly formatted and valid."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Using the gpt-3.5-turbo model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,  # Adjust the response length if needed
        temperature=0.7  # Adjust the creativity level of the response
    )
    
    # Extract and parse the response text
    response_text = response.choices[0].message['content'].strip()
    if response_text.startswith('```'):
        response_text =  response_text[7:-3]
    try:
        response_dict = json.loads(response_text)
    except json.JSONDecodeError:
        print(response_text)
        response_dict = {"error": "Failed to parse response as JSON", "raw_response": response_text}
    
    return response_dict

def get_ai_response_feedback(question, code):
    # Create a prompt that includes the question, query, and option selected by the user
    prompt = (
        f"Question: {question}\n"
        f"code given by user: {code}\n\n"
        "Provide the following in JSON format:\n"
        "{\n"
        "  \"answer\": \"<the correct code answer to the question if the given code is incorrect, the improve code if the given code can be improves, original code itself if nothing need to be changed>\",\n"
        "  \"explanation\": \"<a detailed feedback of the code with repsect to the given question which must contain informations like if it is correct or incorrect, what needs to be improved etc. >\"\n"
        "}\n"
        "Ensure that the JSON is properly formatted and valid."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Using the gpt-3.5-turbo model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,  # Adjust the response length if needed
        temperature=0.7  # Adjust the creativity level of the response
    )
    
    # Extract and parse the response text
    response_text = response.choices[0].message['content'].strip()
    if response_text.startswith('```'):
        response_text =  response_text[7:-3]
    try:
        response_dict = json.loads(response_text)
    except json.JSONDecodeError:
        print(response_text)
        response_dict = {"error": "Failed to parse response as JSON", "raw_response": response_text}
    
    return response_dict

