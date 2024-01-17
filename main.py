from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'PUT'])
def webhook():
    pretty_json = json.dumps(request.json, indent=4)
    print(pretty_json)
    return "Webhook received!", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)