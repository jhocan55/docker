import os
import requests

# Definition of the API address and port
api_address = 'api'  # changed from 'localhost'
api_port = 8000

# Test scenarios
scenarios = [
    ('alice', 'wonderland', 'v1', 200),
    ('alice', 'wonderland', 'v2', 200),
    ('bob', 'builder', 'v1', 200),
    ('bob', 'builder', 'v2', 403)
]

# Template for output
output_template = '''
============================
    Authorization test
============================

Request done at "/{endpoint}"
| username="{username}"
| password="{password}"

Expected result = {expected_status}
Actual result   = {actual_status}

==>  {test_status}

'''

logs = ''

# Loop through scenarios and perform requests
for username, password, endpoint, expected_status in scenarios:
    try:
        # Perform the request
        r = requests.get(
            url=f'http://{api_address}:{api_port}/{endpoint}/sentiment',
            params={
                'username': username,
                'password': password,
                'sentence': 'test'
            },
            timeout=5  # Prevent hanging requests
        )
        # Determine test status
        actual_status = r.status_code
        test_status = 'SUCCESS' if actual_status == expected_status else 'FAILURE'
    except requests.RequestException as e:
        # Handle request exceptions
        actual_status = 'ERROR'
        test_status = 'FAILURE'
        logs += f"Error during request for user '{username}' at endpoint '{endpoint}': {str(e)}\n"
    else:
        # Format the output
        output = output_template.format(
            endpoint=endpoint,
            username=username,
            password=password,
            expected_status=expected_status,
            actual_status=actual_status,
            test_status=test_status
        )
        logs += output

# Print logs to console
print(logs)

# Write logs to a file if the LOG environment variable is set
if os.environ.get('LOG') == '1':
    try:
        with open('/app/logs/api_test.log', 'a') as file:  # changed log file path
            file.write(logs)
    except IOError as e:
        print(f"Failed to write logs to file: {e}")