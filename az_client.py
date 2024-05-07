import time
from openai import AzureOpenAI
from config import AZURE_OPENAI_KEY, AZURE_OPENAI_BASE_URL, EMBED_MODEL
import json
import tiktoken

azure_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_OPENAI_BASE_URL
)

def correct_length(text: str) -> str:
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    tokens = tokens[:8190]  # Truncate the tokens to the max_tokens length
    vector_safe = encoding.decode(tokens)   
    return vector_safe


def get_vector(text):
    retries = 10
    safe_text = correct_length(text)
    for attempt in range(retries):
        try:            
            embeddings = azure_client.embeddings.create(input = safe_text, model=EMBED_MODEL).data[0].embedding                                               
            return embeddings        
        except Exception as e:
            print(f"Error: {e}")
            if attempt < retries - 1:  # i is zero indexed
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            else:
                # if exception persists even after 10 attempts
                raise

# Parses the JSON from a function call, if there is an error in JSON parsing, recalls the LLM with the fix json function to get a valid json response.
def parse_JSON(json_str: str) -> dict:        
    try: 
        return json.loads(json_str)
    except Exception as e:              
        messages = [
      {
        'role': 'system',
        'content':
          'Assistant is a large language model designed to fix and return correct JSON objects.',
      },
      {
        'role': 'user',
        'content': f'ORIGINAL ERROR CONTAINING JSON OBJECT:\n\n{json_str}\n\nERROR MESSAGE: {e}',
      },
    ]
        
        tool_choices = [{
      'type': 'function',
      'function': {
        'name': 'fix_object',
        'description':
          'You will be given an incorrectly formed JSON Object and a error message. You must fix the incorrect JSON Object and return the valid JSON object.',
        'parameters': {
          'type': 'object',
          'properties': {
            'fixedJSON': {
              'type': 'string',
              'description': 'The reformated and error free JSON object. Return the JSON object only!',
            },
          },
          'required': ['fixedJSON'],
        },
      },
    }]                
        response = azure_client.chat.completions.create(
                    model='gpt-4',
                    messages=messages,                    
                    max_tokens=4096,
                    temperature=0,
                    tools=tool_choices,
                    tool_choice={ 'type': 'function', 'function': { 'name': 'fix_object' } },        
                )        
                
        second_test_json = response.choices[0].message.tool_calls[0].function.arguments 
                  
        to_return = json.loads(second_test_json)
        return json.loads(to_return['fixedJSON'])

def call_ai(prompt: str, function: dict) -> dict:
    message_arr = [{"role": "user", "content": prompt}]    
    try:                
        response = azure_client.chat.completions.create(
                        model='gpt-4',
                        messages=message_arr,
                        max_tokens=4096,
                        temperature=0,
                        tools=[function],
                    )
        json_res = parse_JSON(response.choices[0].message.tool_calls[0].function.arguments)        
        return json_res
    except Exception as e:
        print(e)
        return "\n***\n"