import time
from openai import OpenAI
import json
import tiktoken
from config import OPENAI_KEY, TXT_MODEL, EMBEDDING_MODEL, DEFAULT_TXT_PARAMS

client = OpenAI(
    api_key=OPENAI_KEY,        
)

def correct_length(text: str, max_tokens = 8190, model = 'gpt-4o' ) -> str:
    if model == "gpt-4o":
        encoding = tiktoken.encoding_for_model("gpt-4o")
    else:
        encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    tokens = tokens[:max_tokens] # Truncate the tokens to the max_tokens length
    vector_safe = encoding.decode(tokens)
    return vector_safe

def get_vector(text):
    retries = 10
    safe_text = correct_length(text)
    for attempt in range(retries):
        try:            
            embeddings = client.embeddings.create(input = safe_text, model=EMBEDDING_MODEL).data[0].embedding                                               
            return embeddings        
        except Exception as e:
            print(f"Error: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            else:                
                raise e

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
        additional_params = {
          'messages': messages,
          'tools': tool_choices,
          'tool_choice':{ 'type': 'function', 'function': { 'name': 'fix_object' } }
          }
        params = {**DEFAULT_TXT_PARAMS, **additional_params} 
        response = client.chat.completions.create(params)
                
        second_test_json = response.choices[0].message.tool_calls[0].function.arguments 
                  
        to_return = json.loads(second_test_json)
        return json.loads(to_return['fixedJSON'])

def call_ai(message_arr: list, function: dict) -> dict:    
    additional_params = {
    'messages': message_arr,
    'tools': [function]
    }
    params = {**DEFAULT_TXT_PARAMS, **additional_params} 
    try:                
        response = client.chat.completions.create(**params)
        json_res = parse_JSON(response.choices[0].message.tool_calls[0].function.arguments)        
        return json_res
    except Exception as e:        
        raise e