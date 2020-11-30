from flask import Flask, request, jsonify
import mail

app = Flask(__name__)
app.config['DEBUG'] = True

m = mail.Mail()

@app.route('/send', methods=['POST'])
def send():
    body = request.json
    to = body['to']
    subject = body['subject']
    message = body['message']
    
    try:
        if m.send(to, subject, message):
            return jsonify({"status": "200", "message": "Success sent email"})
        else:
            return jsonify({"status": "500", "message": "Fail sent email"})

    except Exception as e:
        print("ERROR WHILE SEND MAIL")
        print(e)
        return jsonify({"status": "500", "message": "Error occured when sent email"})

@app.route('/inbox', methods=['GET'])
def inbox():
    page = request.args.get('page')
    if (page is None): page = 1
    try:
        data = m.inbox(page)
        return jsonify({"status": "200", "message": "Success get inbox", "data": data})

    except Exception as e:
        print("ERROR WHILE SEND MAIL")
        print(e)
        return jsonify({"status": "500", "message": "Error occured when get inbox"})

if __name__ == '__main__':
    app.run(debug=True)