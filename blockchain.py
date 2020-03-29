import hashlib
import time
import json


class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.transaction_pool = []
        self.create_block(previous_hash='Initialize')

    def make_hash(self, block):
        json_block = json.dumps(block)
        return hashlib.sha256(json_block.encode()).hexdigest()

    def create_block(self, previous_hash=None, nonce=0, transaction=None, timestamp=time.time()):
        block = {
            'previous_hash': previous_hash,
            'nonce': nonce,
            'transaction': transaction,
            'timestamp': timestamp
          }
        self.add_block_to_chain(block)

    def add_block_to_chain(self, block):
        self.chain.append(block)

    def mining(self):
        previous_hash = self.make_hash(self.chain[-1])
        nonce = 0
        transaction = self.transaction_pool
        self.transaction_pool = []
        while True:
            if self.proof_of_work(previous_hash, nonce, transaction):
                break
            else:
                nonce += 1
        timestamp = time.time()
        self.create_block(previous_hash, nonce, transaction, timestamp)

    def proof_of_work(self, previous_hash, nonce, transaction):
        guess_block = {
          'previous_hash': previous_hash,
          'nonce': nonce,
          'transaction': transaction
        }
        guess_hash = self.make_hash(guess_block)
        return guess_hash.startswith('0'*2)

    def add_transaction(self, sender_name, recipient_name, value):
        transaction = {
            'sender_name': sender_name,
            'recipient_name': recipient_name,
            'value': value
        }
        self.transaction_pool.append(transaction)

    def print_chain(self):
        for chain_index, block in enumerate(self.chain):
            print(f'{"="*40}Block {chain_index:3}')
            if block['transaction'] is None:
                print('Initialize')
                continue
            else:
                for key, value in block.items():
                    if key == 'transaction':
                        for transaction in value:
                            print(f'{"transaction":15}:')
                            for kk, vv in transaction.items():
                                print(f'\t{kk:15}:{vv}')
                    else:
                        print(f'{key:15}:{value}')

    def check_falsification(self):
        print('=' * 30 + 'Check falsification')
        for chain_index, block in enumerate(self.chain):
            if chain_index == 0:
                continue
            else:
                if block['previous_hash'] != self.make_hash(self.chain[chain_index-1]):
                    print(f'[Block {chain_index-1}]Falsification is detected!!')
                    return
        print('There is no falsification')


if __name__ == '__main__':
    # print('='*30 + 'Start' + '='*30)
    blockchain = BlockChain()
    blockchain.add_transaction(sender_name='Alice', recipient_name='Bob', value=100)
    blockchain.add_transaction(sender_name='Alice', recipient_name='Chris', value=1)
    blockchain.mining()
    blockchain.add_transaction(sender_name='Bob', recipient_name='Dave', value=100)
    blockchain.mining()
    blockchain.add_transaction(sender_name='Chris', recipient_name='Dave', value=100)
    blockchain.mining()
    blockchain.chain[2]['transaction'][0]['value'] = 10000
    blockchain.print_chain()
    blockchain.check_falsification()