from flask import *
import hmac, hashlib, base64
import time, requests, json

@app.route("/sendsms", methods=["GET"])
def send_sms():
sid = "ncp:sms:kr:254261821659:danim-test" sms_uri = "/sms/v2/services/"+sid+"/messages".format(sid) sms_url = "https://sens.apigw.ntruss.com{}".format(sms_uri) acc_key_id = "rahaKHMHEDHe7k66FoMk" acc_sec_key = b'ViNW1KD4cf5EJkoJm1rSTtarJ7s2FlyaM0aVuUF9'
    stime = int(float(time.time()) * 1000)
    hash_str = "POST {}\n{}\n{}".format(sms_uri, stime, acc_key_id)
    digest = hmac.new(acc_sec_key, msg=hash_str.encode('utf-8'), digestmod=hashlib.sha256).digest()
    d_hash = base64.b64encode(digest).decode()
    from_no = "01097196521"
    to_no   = request.args.get('to')
    sender = request.args.get('sender')
    link = request.args.get('link')
    message = "당신을 행복하게 만들어줄," + sender + "님의 여행 선물이 도착했어요!\n" + link + "링크를 눌러서 확인하세요!"
    msg_data = {
        'type': 'SMS',
        'countryCode': '82',
        'from': "{}".format(from_no),
        'contentType': 'COMM',
        'content': "{}".format(message),
        'messages': [{'to': "{}".format(to_no)}]
    }
    response = requests.post(
        sms_url, data=json.dumps(msg_data),
        headers={"Content-Type": "application/json; charset=utf-8",
                "x-ncp-apigw-timestamp": str(stime),
                "x-ncp-iam-access-key": acc_key_id,
                "x-ncp-apigw-signature-v2": d_hash
                })
    print(response.text)
    return '200'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)