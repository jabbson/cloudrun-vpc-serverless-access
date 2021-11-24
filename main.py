import os
import socket

from flask import Flask, request, render_template
app = Flask(__name__)


def test(host, port):
    timeout_seconds=3

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_seconds)
    result = sock.connect_ex((host,int(port)))
    sock.close()
    return "SUCCESS" if result == 0 else "FAIL"

@app.route("/")
def root():
    return 'CLOUD RUN INSTANCE IS UP, try <a href="/test">/test</a> now.'

@app.route("/test", methods=["GET", "POST"])
def test_redis():
    result = ''
    host = ''
    port = ''

    if request.method == "POST":
        host = request.form.get('host')
        port = request.form.get('port')
        result = test(host, port)

    return render_template('index.html', result=result, host=host, port=port)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
