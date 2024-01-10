from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'PUT'])
def webhook():
    if request.method == 'POST':
        print("Received a POST request:")
    elif request.method == 'PUT':
        print("Received a PUT request:")
    print(request.json)
    return "Webhook received!", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
