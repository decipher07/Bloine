import functools 
import hashlib 
import json 
import pickle

from hash_util import hash_string_256, hash_block
from block import Block 
from transaction import Transaction 


blockchain = []

open_transactions = [] 

MINING_REWARD = 10 

owner = 'DJ'

def load_data():
    global blockchain
    global open_transactions
    try :
        with open('blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            
            file_content = f.readlines()



            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:

                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]

                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'] )
                
                updated_blockchain.append(updated_block)

            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = [] 
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except(IOError, IndexError):

        genesis_block = Block(0, '', [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []
        print('File Not Found')
    finally:
        print('Clean Up')
load_data()

def save_data():
    try :
        with open('blockchain.txt', mode='w') as f:
            savable_chain = [block.__dict__ for  block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el  in blockchain ]]
            f.write(json.dumps(savable_chain))
            f.write('\n')
            savable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(savable_tx))
        # save_data = {
        #     'chain': blockchain,
        #     'ot': open_transactions
        # }
        # f.write(pickle.dumps(save_data))
    except (IOError):
        print('Saving Failed')

 
def valid_proof(transactions, last_hash, proof):
    guess = ( str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess) 
    print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash =  hash_block(last_block)
    proof = 0 
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1 
    return proof 



def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = functools.reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else  tx_sum+0 , tx_sender, 0)

    # amount_sent = 0 
    # for tx in tx_sender :
    #     if len(tx) > 0 :
    #         amount_sent += tx[0]
    # amount_received = 0 
    # for tx in tx_recipient :
    #     if len(tx) > 0 :
    #         amount_received += tx[0]
    
    
    tx_recipient  = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
 
    amount_received = functools.reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else  tx_sum+0    , tx_recipient, 0)


    return amount_received - amount_sent

def get_last_blockchain_value():
    if len(blockchain) < 1 :
        return None 
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount

def add_transaction( recipient,sender=owner, amount=1.0):
    
    
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount    
    # }

    transaction = Transaction(sender, recipient, amount)

    if verify_transaction(transaction):
        open_transactions.append(transaction)   
        save_data()
        return True 
    return False 


def mine_block():
    last_block = blockchain[-1]
    hashed_block =  hash_block(last_block)
    
    proof = proof_of_work()

    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD,
    # }  

    reward_transaction = Transaction('MINING', owner, MINING_REWARD)    
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof )
    blockchain.append(block)
    return True 
    
def get_transaction_value():
    
    tx_recipient = input ('Enter The Recipient Of the Transaction ')

    tx_amount = float(input('Your Transaction Amount Please:'))
    return (tx_recipient, tx_amount)

def get_user_choice():
    user_input = input('Your Choice :')
    return user_input

def print_blockchain_elements():
    for block in blockchain:
        print ('Outputting The Block')
        print(block)
    

def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0 :
            continue 
        if block.previous_hash !=  hash_block( blockchain[index-1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof ):
            print('Proof of Work is Invalid')
            return False 
    return True 



def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
    # is_valid = True 
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid=True 
    #     else :
    #         is_valid = False 
    
    # return is_valid  


waiting_for_input = True 

while waiting_for_input:
    print('Please Choose')
    print ('1: Add a New Transaction Value ')
    print ('2: Mine a new Block ')
    print ('3: Output the Blockchain Blocks')
    print ('4: Check Transaction Validity')
    print ('q: Quit')
    
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data 
        
        if add_transaction(recipient, amount = amount):
            print(open_transactions)
        else :
            print('Transaction Failed')
        print(open_transactions)
    elif user_choice == '2' :
       if mine_block():
           open_transactions = []
           save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        if verify_transactions():
            print('All Transactions are Valid')
        else :
            print('There are Invalid Transactions')
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print ('Input was Invalid , Please Pick a Value From the List ')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid Blockchain !')
        break
    print('Balance of {} : {:6.2f}'.format('DJ', get_balance('DJ'))) 
else :
    print('User Left !')    
