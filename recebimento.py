from time import time
import json
import hashlib
from uuid import uuid4
from urllib.parse import urlparse
from categorias import Categoria
from flask import Flask, jsonify, request


class BlockChain(object):
    """ Classe Principal que Representa a BlockChain """

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.validations_nodes = set()

        self.new_block(previous_hash=123, proof=100)

    def new_block(self, proof, previous_hash=None):
        """ Metodo responsavel pela criação de novos blocos """
        block = {'index': len(self.chain) + 1,
                 'timestamp': time(),
                 'transactions': self.current_transactions,
                 'proof': proof,
                 'previous_hash': previous_hash or self.hash(self.last_block)}

        # Validar Bloco
        self.current_transactions = []

        self.chain.append(block)
        return block

    @property
    def pending_transactions(self):
        """ Todas as transações aguardando serem realizadas """
        return self.current_transactions

    @property
    def transactions(self):
        """ Todas as transações realizadas na chain """
        return [block['transactions'] for block in self.chain]

    @property
    def full_transactions(self):
        """ Todas as transações existentes """
        return self.transactions() + self.pending_transactions()

    def new_transaction(self, categoria, notas, empresa):
        """ Metodo responsável por criar uma nova transação """
        transaction = {'empresa': empresa,
                       'categoria': categoria,
                       'notas': notas,
                       'horario': time()}

        self.current_transactions.append(transaction)
        return int(self.last_block['index']) + 1

    @property
    def blocks(self):
        """ Todos os blocos na chain """
        return self.chain

    @property
    def last_block(self):
        """ Metodo responsavel por encontrar o ultimo bloco da chain"""
        return self.chain[-1]

    def full_chain(self):
        """ Metodo responsavel por retornar toda a chain e o tamanho dela """
        return self.chain, len(self.chain)

    def proof_of_work(self, last_proof):
        """ Metodo responsavel por gerar o proof of work """
        proof = 0
        while self.validate_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def register_nodes(self, address):
        """ Metodo responsavel por registrar os nós de validação """
        parsed_address = urlparse(address)
        self.nodes.add(parsed_address.netloc)

    @ staticmethod
    def validate_proof(last_proof, current_proof):
        """ Metodo responsavel por validar o proof """
        proof = f'{last_proof}{current_proof}'.encode()
        proof_hash = hashlib.md5(proof).hexdigest()
        return proof_hash[:4] == '0010'

    @ staticmethod
    def hash(block):
        """ Metodo responsavel por criar o hash do bloco """
        block_str = json.dumps(block, sort_keys=True).encode()  # obj -> string
        return hashlib.md5(block_str).hexdigest()


app = Flask(__name__)
app.testing = True
blockChain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')


@app.route('/mining', methods=['GET'])
def mining():
    last_block = blockChain.last_block
    last_proof = last_block['proof']

    proof = blockChain.proof_of_work(last_proof)
    previous_hash = blockChain.hash(last_block)
    block = blockChain.new_block(proof, previous_hash)

    # Validações para o bloco

    response = {
        'message': 'New block created',
        'index': block['index'],
        'proof': block['proof']}

    return jsonify(response, 200)


@app.route('/transaction/new', methods=['GET'])
def new_transaction():
    params = request.get_json()
    transaction_idx = blockChain.new_transaction(
        categoria=params['categoria'], notas=params['notas'], empresa=params['empresa'])

    response = {
        'message': 'New transaction created',
        'index': transaction_idx,
        'transaction': blockChain.pending_transactions[-1]
    }

    return jsonify(response, 200)


@app.route('/last', methods=['GET'])
def last_block():
    last_block = blockChain.last_block
    response = {'index': last_block['index'],
                'timestamp': last_block['timestamp'],
                'transactions': last_block['transactions'],
                'proof': last_block['proof'],
                'previous_hash': last_block['previous_hash']}
    return jsonify(response, 200)


@app.route('/nodes/register', methods=['GET'])
def register_nodes():
    params = request.get_json()
    for node in params['nodes']:
        blockChain.register_nodes(node)

    response = {
        'message': 'New nodes registered',
        'ammount': len(params['nodes'])
    }
    return jsonify(response, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# main_class = Main()
# transaction_idx = main_class.new_transaction(
#     categoria=Categoria.ENTRADA, empresa='Unilever', notas=['123', '497'])
# print(f'O id da transação é {transaction_idx}')
# new_block = main_class.mining()
# proof = new_block['proof']
# print(f'O proof do bloco é {proof}')
# print(main_class.blockChain.last_block)
