import os, requests
from flask import Flask, request
import shopify

app = Flask(__name__)

API_KEY='338b5bb3d617f65e31c4d9b0b52e79fb'
SHARED_SECRET='067daa1397008d51b55d8ffc4612390d'
STORE_NAME='ashudemo.myshopify.com'
scope=["read_orders"]


shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)

session = shopify.Session(STORE_NAME)
debug = False if os.environ['APP_ENV'] == 'production' else True

@app.route('/')
def hello():
    global session
    code = request.args.get('code')
    if code:
        token = session.request_token(request.args)
        session = shopify.Session(STORE_NAME, token)
        shopify.ShopifyResource.activate_session(session)
        return token
    else:
        return '<a href="{0}">Click here to authorize</a>'.format('/auth')

@app.route('/auth')
def auth():
    global session
    permission_url = session.create_permission_url(scope,"https://e7184d84.ngrok.io")
    return permission_url

@app.route('/list')
def listOrders():
    shopify.ShopifyResource.activate_session(session)
    print("Getting order...", activator)
    order = shopify.Order.find(610481471588)
    print("Got order")
    return type(order)
#    return order.email.decode('utf-8')
if __name__ == '__main__':
    print("Server running at"+ os.environ['HOST'] +":"+ os.environ['PORT'])
    app.run(host=os.environ['HOST'], port=os.environ['PORT'], debug=debug)
