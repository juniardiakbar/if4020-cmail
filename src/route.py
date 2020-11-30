from flask import Flask, request, jsonify
import mail

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/send', methods=['POST'])
def send():
    body = request.json
    to = body['to']
    subject = body['subject']
    message = body['message']
    
    try:
        if mail.send(to, subject, message):
            return jsonify({"status": "200", "message": "Success sent email"})
        else:
            return jsonify({"status": "500", "message": "Fail sent email"})

    except Exception as e:
        print("ERROR WHILE SEND MAIL")
        print(e)
        return jsonify({"status": "500", "message": "Error occured when sent email"})


if __name__ == '__main__':
    app.run(debug=True)