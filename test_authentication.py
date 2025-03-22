import os
import requests

api_address = 'api'
api_port = 8000

users = [
    ('alice', 'wonderland', 200),
    ('bob', 'builder', 200),
    ('clementine', 'mandarine', 403)
]

logs = ''
for username, password, expected_status in users:
    try:
        r = requests.get(
            url=f'http://{api_address}:{api_port}/permissions',
            params={'username': username, 'password': password},  # Fixed: use params instead of auth
            timeout=5
        )
        code = r.status_code
    except requests.RequestException as e:
        code = 'ERROR'
        logs += f"Test Authentication: Error for user '{username}': {str(e)}\n"
        continue
    status = 'SUCCESS' if code == expected_status else 'FAILURE'
    log_entry = f"""
Test Authentication:
User: {username}
Expected: {expected_status}, Got: {code}
Result: {status}
"""
    logs += log_entry

if os.environ.get('LOG') == '1':
    with open('/app/logs/api_test.log', 'a') as file:
        file.write(logs)
