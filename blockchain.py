import functools 
import hashlib 
import json 
import pickle

from utils.hash_util import hash_block
from utils.verification import Verification
from block import Block 
from transaction import Transaction 
from wallet import Wallet 

MINING_REWARD = 10 

class Blockchain:
    
    def __init__(self, hosting_node_id):

        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = [] 
        self.load_data()
        self.hosting_node = hosting_node_id
        self.__peer_nodes = set()
    
    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val 
    
    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):

        try :
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                
                file_content = f.readlines()



                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']

                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:

                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]

                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'] )
                    
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = [] 
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except(IOError, IndexError):
            pass 
            print('Handled Exceptions')
        finally:
            print('Clean Up')


    def save_data(self):
        try :
            with open('blockchain.txt', mode='w') as f:
                savable_chain = [block.__dict__ for  block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el  in self.__chain ]]
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
        except (IOError):
            print('Saving Failed')

    

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash =  hash_block(last_block)
        proof = 0 
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1 
        return proof 



    def get_balance(self):

        if self.hosting_node == None:
            return None 

        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
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
        
        
        tx_recipient  = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
    
        amount_received = functools.reduce(lambda tx_sum, tx_amt : tx_sum + sum(tx_amt) if len(tx_amt) > 0 else  tx_sum+0    , tx_recipient, 0)


        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1 :
            return None 
        return self.__chain[-1]


    def add_transaction( self, recipient,sender, signature,amount=1.0):
        
        
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount    
        # }

        if self.hosting_node == None :
            return False 
        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)   
            self.save_data()
            return True 
        return False 


    def mine_block(self):
        if self.hosting_node == None :
            return None 
        last_block = self.__chain[-1]
        hashed_block =  hash_block(last_block)
        
        proof = self.proof_of_work()

        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)    
        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None 

        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof )
        
      
        
        self.__chain.append(block)

        self.__open_transactions = []
        self.save_data()

        return block 

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()    
    
    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()
    
    def get_peer_nodes(self):

        return list(self.__peer_nodes)


        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD,
        # }  


    # is_valid = True 
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid=True 
    #     else :
    #         is_valid = False 
    
    # return is_valid  

