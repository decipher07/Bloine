from flask import Flask 
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
Blockchain = Blockchain(wallet.public_key)
CORS(app)

@app.route('/', methods=['GET'])
def get_ui():
    return 'This Works!'

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
