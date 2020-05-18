blockchain = []
open_transactions = []

def get_last_blockchain_value():
    if len(blockchain) < 1 :
        return None 
    return blockchain[-1]


def add_transaction(sender, recipient, amount=1.0):
    transaction = {'sender': sender,
                    'recipient': recipient,
                    'amount': amount    
                    }
    open_transactions.append()
    


def mine_block():
    pass 

def get_transaction_value():
    user_input = float(input('Your Transaction Amount Please:'))
    return user_input

def get_user_choice():
    user_input = input('Your Choice :')
    return user_input

def print_blockchain_elements():
    for block in blockchain:
        print ('Outputting The Block')
        print(block)
    else :
        print('-' * 20 )


def verify_chain():
    is_valid = True 
    for block_index in range(len(blockchain)):
        if block_index == 0 :
            continue 
        elif blockchain[block_index][0] == blockchain[block_index-1]:
            is_valid = True 
        else:
            is_valid = False  
