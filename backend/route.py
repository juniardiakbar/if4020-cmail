from flask import Flask, request, jsonify
from flask_cors import cross_origin
import mail

app = Flask(__name__)
app.config['DEBUG'] = True

m = mail.Mail()

@app.route('/send', methods=['POST'])
@cross_origin(origin='localhost')
def send():
    body = request.json
    to = body['to']
    subject = body['subject']
    message = body['message']
    
    try:
        m.send(to, subject, message)
        return jsonify({"status": "200", "message": "Success sent email"})
        
    except Exception as e:
        print("ERROR WHILE SEND MAIL")
        print(e)
        return jsonify({"status": "500", "message": "Error occured when sent email"})

@app.route('/inbox', methods=['GET'])
@cross_origin(origin='localhost')
def inbox():
    page = request.args.get('page')
    if (page is None): page = 1
    try:
        data = m.inbox(page)
        return jsonify({"status": "200", "message": "Success get inbox", "data": data})

    except Exception as e:
        print(e)
        return jsonify({"status": "500", "message": "Error occured when get inbox"})

@app.route('/sent', methods=['GET'])
@cross_origin(origin='localhost')
def sent():
    page = request.args.get('page')
    if (page is None): page = 1
    try:
        data = m.sent(page)
        return jsonify({"status": "200", "message": "Success get sent mail", "data": data})

    except Exception as e:
        print(e)
        return jsonify({"status": "500", "message": "Error occured when get sent mail"})

if __name__ == '__main__':
    app.run(debug=True)