from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"products": ["Product A", "Product B", "Product C"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
