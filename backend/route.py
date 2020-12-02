from flask import Flask, request, jsonify
from flask_cors import cross_origin
import mail
import os
from dotenv import load_dotenv
import algorithms.feistel as feistel
import algorithms.sm2_dsa as sign

app = Flask(__name__)
app.config['DEBUG'] = True

email = os.getenv("EMAIL")
m = mail.Mail()
s = sign.SM2_DSA()

@app.route('/send', methods=['POST'])
@cross_origin(origin='localhost')
def send():
    body = request.json
    to = body['to']
    subject = body['subject']
    message = body['message']
    encrypt_key = body['encryptKey']
    encrypt_mode = body['encryptMode']
    signature = body['signature']
    signature_key = body['signatureKey']
    enc = False

    try:
        if (encrypt_key != "" and encrypt_mode != ""):
            enc = True
            subject = "ENC - " + subject 
            message = feistel.encrypt(encrypt_key, message, encrypt_mode)

        if (signature):
            if (enc): subject = "DGENC - " + subject
            else: subject = "DG - " + subject
            
            message_byte = str.encode(message)
            uid = str.encode(email)
            sign = s.sign(message_byte, uid, signature_key)
            sign_str = str(int.from_bytes(sign[0], "little")) + ';' + str(int.from_bytes(sign[1], "little"))

            message += "\n\n--BEGIN SIGNATURE SIGN--\n"
            message += sign_str
            message += "\n--END SIGNATURE SIGN--"

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
    encrypt_key = request.args.get('encryptKey')
    encrypt_mode = request.args.get('encryptMode')

    if (page is None): page = 1
    try:
        data = m.inbox(page, encrypt_key, encrypt_mode)
        return jsonify({"status": "200", "message": "Success get inbox", "data": data})

    except Exception as e:
        print(e)
        return jsonify({"status": "500", "message": "Error occured when get inbox"})

@app.route('/sent', methods=['GET'])
@cross_origin(origin='localhost')
def sent():
    page = request.args.get('page')
    encrypt_key = request.args.get('encryptKey')
    encrypt_mode = request.args.get('encryptMode')
    
    if (page is None): page = 1
    try:
        data = m.sent(page, encrypt_key, encrypt_mode)
        return jsonify({"status": "200", "message": "Success get sent mail", "data": data})

    except Exception as e:
        print(e)
        return jsonify({"status": "500", "message": "Error occured when get sent mail"})

if __name__ == '__main__':
    app.run(debug=True)