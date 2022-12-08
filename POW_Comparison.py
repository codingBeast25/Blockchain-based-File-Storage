# file to compare two different Proof of work algorithms implemented in the Main source code for blockchain
# first algorithm generates nonce using random function
# second algorithm simply increments nonce by 1 after each iteration of generating valid hash value

from Blockchain import Blockchain
from Block import Block
from timeit import default_timer as timer
import random
import string
import threading

pow_run = [] # to store running time of pow algorithm with various difficulty levels
pow2_run = [] # to store running time of pow2 algorithm with various difficulty levels


# generates random string
def random_char(y):
    return ''. join(random. choice(string. ascii_letters) for x in range(y))


# this is method add transactions to the block on the fly make it more realistic
def add_transaction(block):

   global transactions_length
   global transactions
   
   for i in range(transactions_length):
    
    
    if(random.random() > 0.9):
    
            
        name = random_char(random.randint(0,20))
        file_name = random_char(random.randint(0,20))
        file_data = random_char(random.randint(0,200))
        
        t = {

            "user" : name,
            "v_file" : file_name,
            "file_data" : file_data,
            "file_size" : random.randint(0,1000) 
        } 

        block.add_t(t)
# run pow algorithms  with difficulty from 2 to 5
for j in range(2,6):

    block_index = random.randint(0,2000)
    transactions_length = random.randint(10,20)
    transactions = []

    # creates random block      
    b = Block(block_index,transactions,"0")
    chain = Blockchain()
    Blockchain.difficulty = j
    
    # thread to add transactions on the fly    
    new_thread = threading.Thread(target=add_transaction, args= (b,))
    new_thread.start()

    # calculating running time for POW algorithm     
    start = timer()
    print(chain.p_o_w(b))
    end = timer()
    print(end-start)
    pow_run.insert(j, end-start)

    # calculating running time for POW2 algorithm     
    start = timer()
    print(chain.p_o_w_2(b))
    end = timer()
    print(end-start)
    pow2_run.insert(j, end-start)


print("------------Proof of Work with Random Nounce ------------")
for a in pow_run:
    print("Difficulty ", pow_run.index(a) + 2, " Time : ", round(a,5))

print("------------Proof of Work with Iterative Nounce ------------")
for a in pow2_run:
    print("Difficulty ", pow2_run.index(a) + 2, " Time : ", round(a,5))

print("------------Proof of Work with Random Nounce ------------")
for a in pow_run:
    print(round(a,5))

print("------------Proof of Work with Iterative Nounce ------------")
for a in pow2_run:
    print(round(a,5))


