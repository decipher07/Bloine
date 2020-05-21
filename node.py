class Node :

    def __init__(self):
        self.blockchain = []


    def get_transaction_value(self):
        
        tx_recipient = input ('Enter The Recipient Of the Transaction ')

        tx_amount = float(input('Your Transaction Amount Please:'))
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        user_input = input('Your Choice :')
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain:
            print ('Outputting The Block')
            print(block)



    def listen_for_input(self):

        waiting_for_input = True 

        while waiting_for_input:
            print('Please Choose')
            print ('1: Add a New Transaction Value ')
            print ('2: Mine a new Block ')
            print ('3: Output the Blockchain Blocks')
            print ('4: Check Transaction Validity')
            print ('q: Quit')
            
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
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
                self.print_blockchain_elements()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(open_transactions,get_balance):
                    print('All Transactions are Valid')
                else :
                    print('There are Invalid Transactions')
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print ('Input was Invalid , Please Pick a Value From the List ')
            verifier = Verification()
            if not verifier.verify_chain(blockchain):
                self.print_blockchain_elements()
                print('Invalid Blockchain !')
                break
            print('Balance of {} : {:6.2f}'.format('DJ', get_balance('DJ'))) 
        else :
            print('User Left !')    
