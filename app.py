from flask import Flask, render_template, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def run_script():
    refresh_token = os.getenv("REFRESH_TOKEN")
    
    if not refresh_token:
        return "Refresh token not found in environment variables."

    headers = {
        'Host': 'api.classplusapp.com',
        'user-agent': 'Mobile-Android',
        'app-version': '1.4.45.1',
        'api-version': '21',
        'device-id': '123',
        'device-details': 'real',
        'region': 'IN',
        'accept-language': 'EN',
        'content-type': 'application/json; charset=UTF-8',
        'accept-encoding': 'gzip',
    }
    
    data = {
        'refreshToken': refresh_token,
        'orgId': 298976
    }

    response = requests.post('https://api.classplusapp.com/users/refreshAccessToken', headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get("data", {}).get("token", "")

        if token:
            token_start_index = token.find("eyJ")
            if token_start_index != -1:
                token = token[token_start_index:]
                print(token)
                return render_template('index.html', token=token)
            else:
                return "Token not found in the response."
        else:
            return "Token not found in the response."
    else:
        return "Request failed with status code:", response.status_code

if __name__ == '__main__':
    app.run(debug=True)
