import os

OPENAI_KEY = os.getenv('OPENAI_KEY')
EMBEDDING_MODEL = 'text-embedding-3-small'
TXT_MODEL = 'gpt-4o-2024-05-13'

DEFAULT_TXT_PARAMS = {'model': TXT_MODEL, 'frequency_penalty': 0, 'max_tokens': 4096, 'presence_penalty': 0, 'temperature': 1e-9, 'top_p': 1e-9}

API_KEY = os.getenv('API_KEY')

PASSWORD_COOKIE_NAME = "ACMA_Res_password"
