genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

blockchain = [genesis_block]
open_transactions = []
owner = 'DJ'



def get_last_blockchain_value():
    if len(blockchain) < 1 :
        return None 
    return blockchain[-1]


def add_transaction( recipient,sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount    
    }
    open_transactions.append(transaction)
    


def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''
    for key in last_block :
        value = last_block[key]
        hashed_block = hashed_block + str(value)
    
    print (hashed_block)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)
    
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
    return is_valid

waiting_for_input = True 

while waiting_for_input:
    print('Please Choose')
    print ('1: Add a New Transaction Value ')
    print ('2: Mine a new Block ')
    print ('3: Output the Blockchain Blocks')
    print ('h: Maniputlate The Chain ')
    print('q: Quit')
    
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data 
        add_transaction(recipient , amount = amount)

        print(open_transactions)

    elif user_choice == '2' :
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print ('Input was Invalid , Please Pick a Value From the List ')