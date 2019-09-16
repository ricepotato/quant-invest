import logging
from flask import Flask, jsonify

log = logging.getLogger("app.restapi.flask.basic")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return 'Hello World!'

@app.route("/rec", methods=["GET"])
def rec():
    dict_result = {"msg":"hello world!"}
    return jsonify(dict_result)

@app.route("/error", methods=["GET"])
def error():
    try:
        a = 1 / 0
    except ZeroDivisionError as e:
        return jsonify({"msg":f"error {e}"}), 500

def main():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == '__main__':
    main()