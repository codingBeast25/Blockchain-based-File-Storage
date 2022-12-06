from hashlib import sha256
import json
import random

from flask import Flask, request
import requests



#multiple blocks linked together will make a blockchain
class Block:
    #Each block will include its index, all transactions, and its previous hash
    def __init__(self, index, transactions, prev_hash):
        self.index = index  # index of each block
        self.transactions = transactions # transactions (information about files stored in a block)
        self.prev_hash = prev_hash # hash of the previous block. 
        self.nonce = 0 # nonce useful for mining new block using POW consensus


    # creates a hash for the block
    def generate_hash(self):

        #  generates hash code using the values stored in block instance. completely random  
        all_data_combined = str(self.index) + str(self.nonce) + self.prev_hash + str(self.transactions)
        return sha256(all_data_combined.encode()).hexdigest()



#immutable list of blocks
class Blockchain:
    # Difficult for proof of work
    difficulty = 3
    peers_count = 0
    
    def __init__(self):
        self.pending = [] # pending list of data that needs to go on chain.
        self.chain = [] # blockchain
        genesis_block = Block(0, [], "0")
        genesis_block.hash = genesis_block.generate_hash()
        self.chain.append(genesis_block)

        

    # Add a block to the chain after verfying and validating it
    def add_block(self, block, hashl):
        prev_hash = self.last_block().hash
        #check the validity of the block
        if (prev_hash == block.prev_hash and self.is_valid(block, hashl)):
            
            block.hash = hashl
            self.chain.append(block)
            return True
        else:
            return False


    # will add the block to the chain. This method is wrapper for verifying, validating and adding the block
    def mine(self):
        
        if(len(self.pending) > 0):
            last_block = self.last_block()
            # Creates a new block to be added to the chain
            new_block = Block(last_block.index + 1,self.pending,last_block.hash)

            # runs the our proof of work and gets the consensus
            hashl = self.p_o_w(new_block)
            #add the block
            self.add_block(new_block, hashl)
            # Empties the pending list
            self.pending = []
            # Annouce to all peers that new block is added
            announce(new_block)
            # Returns the index of the blockthat was added to the chain
            
            return new_block.index
        else:
            return False

    #generates a proof of work with the stated difficulty if able to mine a block or not, will update the nonce every iteration
    def p_o_w(self, block):
        block.nonce = 0
        get_hash = block.generate_hash()
        while not get_hash.startswith("0" * Blockchain.difficulty):
            block.nonce = random.randint(0,99999999)
            get_hash = block.generate_hash()
        return get_hash

    def p_o_w_2(self, block):
        block.nonce = 0
        get_hash = block.generate_hash()
        while not get_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            get_hash = block.generate_hash()
        return get_hash

    # Adds a new transaction to pending
    def add_pending(self, transaction):
        self.pending.append(transaction)
        
    # Checks if the chain is valid
    @classmethod
    def check_chain_validity(this, chain):
        result = True
        prev_hash = "0"
        
        for block in chain:
            block_hash = block.hash
            
            if this.is_valid(block, block.hash) and prev_hash == block.prev_hash:
                block.hash = block_hash
                prev_hash = block_hash
            else:
                result = False
        return result

    #validity helper method
    @classmethod
    def is_valid(cls, block, block_hash):

        if(block_hash.startswith("0" * Blockchain.difficulty)):

            if(block.generate_hash() == block_hash):
                return True
            else:
                return False
        
        else:
            return False

    # Returns the last Block in the Blockchain
    def last_block(self):
        return self.chain[-1]
# End of Blockchain class



app = Flask(__name__)
blockchain = Blockchain()
peers = []


@app.route("/new_transaction", methods=["POST"])
# new transaction added to the block
def new_transaction():
    file_data = request.get_json()
    
    required_fields = ["user", "v_file", "file_data", "file_size"]
    for field in required_fields:
        if not file_data.get(field):
            return "Transaction does not have valid fields!", 404
    blockchain.add_pending(file_data)
    return "Success", 201

#gets the whole chain
@app.route("/chain", methods=["GET"])
def get_chain():
    consensus()
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    print("Chain Len: {0}".format(len(chain)))
    print("Number of Peers Online: {0}".format(Blockchain.peers_count))
    return json.dumps({"length" : len(chain), "chain" : chain})
        

@app.route("/mine", methods=["GET"])
#Mines pending tx blocks
def mine_uncofirmed_transactions():
    result = blockchain.mine()
    if result:
        return "Block #{0} mined successfully.".format(result)
    else:
        return "There are not transactions to mine"
    


# Adds new peers to the network
def add_peer():
    Blockchain.peers_count+= 1
    nodes = request.get_json()
    if not nodes:
        return "Invalid data", 400
    for node in nodes:
        peers.add(node)
    return "Success", 201

@app.route("/pending_tx")
# Queries uncofirmed transactions
def get_pending_tx():
    return json.dumps(blockchain.pending)


# Alorithm will find the longest chain if any and replace current with new. Helps maintain integrity in chain
def consensus():
    global blockchain
    longest_chain = None
    curr_len = len(blockchain.chain)
    # Check with all peers
    for peer in peers:
        response = request.get("http://{0}".format(peer))
        length = response.json()["length"]
        chain = response.json()["chain"]
        if length > curr_len and blockchain.check_chain_validity(chain):
            curr_len = length
            longest_chain = chain
    if longest_chain:
        blockchain = longest_chain
        return True
    return False


@app.route("/add_block", methods=["POST"])
# Adds a block mined by user to the chain
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],block_data["transactions"],block_data["prev_hash"])
    hashl = block_data["hash"]
    added = blockchain.add_block(block, hashl)
    if not added:
        return "The Block was discarded by the node.", 400
    return "The block was added to the chain.", 201


# Announce to the network once a block has been moned
def announce(block):
    for peer in peers:
        url = "http://{0}/add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))

# Run the Flask web app
app.run(port=8800, debug=True)





