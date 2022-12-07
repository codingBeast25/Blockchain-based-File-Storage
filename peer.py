#import libraries
import json
from Blockchain import Blockchain
from Block import Block
from flask import Flask, request

#app object
app = Flask(__name__)
#blockchain object
blockchain = Blockchain()
#peers list
peers = []

@app.route("/new_transaction", methods=["POST"])
# new transaction added to the block. When user selects to submit new request
def new_transaction():
    file_data = request.get_json() #get json response
    required_fields = ["user", "v_file", "file_data", "file_size"]
    #if any of the fields is missing dont append and throw the message
    for field in required_fields:
        if not file_data.get(field):
            return "Transaction does not have valid fields!", 404
    #else append it to pending transaction
    blockchain.add_pending(file_data)
    return "Success", 201

#gets the whole chain to user if not already displayed
@app.route("/chain", methods=["GET"])
def get_chain():
    # consensus()
    chain = []
    #create a new chain from our blockchain
    for block in blockchain.chain:
        chain.append(block.__dict__)
    #print chain len
    print("Chain Len: {0}".format(len(chain)))
    return json.dumps({"length" : len(chain), "chain" : chain})
        

@app.route("/mine", methods=["GET"])
#Mines pending tx blocks and call mine method in blockchain
def mine_uncofirmed_transactions():
    result = blockchain.mine()
    if result:
        return "Block #{0} mined successfully.".format(result)
    else:
        return "No pending transactions to mine."
    


@app.route("/pending_tx")
# Queries uncofirmed transactions
def get_pending_tx():
    return json.dumps(blockchain.pending)



@app.route("/add_block", methods=["POST"])
# Adds a block mined by user to the chain
def validate_and_add_block():
    block_data = request.get_json() #get the json response
    #create a new block incl its hash
    block = Block(block_data["index"],block_data["transactions"],block_data["prev_hash"])
    hashl = block_data["hash"]
    #append the new block
    added = blockchain.add_block(block, hashl)
    #if not added succesfully
    if not added:
        return "The Block was discarded by the node.", 400
    return "The block was added to the chain.", 201
#run the app
app.run(port=8800, debug=True)
