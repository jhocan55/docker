import os
import requests

api_address = 'api'  # changed from ''
api_port = 8000
phrases = [('life is beautiful', 'positive'), ('that sucks', 'negative')]
versions = ['v1', 'v2']

logs = ''
for version in versions:
    for sentence, sentiment in phrases:
        try:
            r = requests.get(f'http://{api_address}:{api_port}/{version}/sentiment',
                             params={'username': 'alice', 'password': 'wonderland', 'sentence': sentence})
            result = r.json().get('score')
        except requests.RequestException as e:
            logs += f"Test Content: Error for version {version}, sentence '{sentence}': {str(e)}\n"
            continue
        expected = result > 0 if sentiment == 'positive' else result < 0
        status = 'SUCCESS' if expected else 'FAILURE'
        log_entry = f"""
Test Content:
Version: {version}, Sentence: '{sentence}'
Expected sentiment: {sentiment}, Got score: {result}
Result: {status}
"""
        logs += log_entry

if os.environ.get('LOG') == '1':
    with open('/app/logs/api_test.log', 'a') as file:  # changed log file path
        file.write(logs)