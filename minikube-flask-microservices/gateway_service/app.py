from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/aggregated", methods=["GET"])
def get_aggregated_data():
    user_data = requests.get("http://user-service:5000/users").json()
    order_data = requests.get("http://order-service:5000/orders").json()
    product_data = requests.get("http://product-service:5000/products").json()
    
    return jsonify({
        "users": user_data,
        "orders": order_data,
        "products": product_data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
