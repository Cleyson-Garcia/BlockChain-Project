from time import time
import json
import hashlib
from categorias import Categoria


class BlockChain(Object):
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
                 'previous_hash': previous_hash or self.hash(self.last_block())}

        # Validar Bloco
        self.current_transactions = []

        self.chain.append(block)
        return block

    def transactions(self):
        """ Todas as transações aguardando serem realizadas """
        return self.current_transactions

    def full_transactions(self):
        """ Todas as transações realizadas na chain """
        return [block['transactions'] for block in self.chain]

    def new_transaction(self, categoria, notas, placa):
        """ Metodo responsável por criar uma nova transação """
        transaction = {'categoria': categoria,
                       'horario': time(),
                       'notas': notas,
                       'placa': placa}

        self.current_transactions.append(transaction)

    def blocks(self):
        """ Todos os blocos na chain """

    def last_block(self):
        """ Metodo responsavel por encontrar o ultimo bloco da chain"""
        return self.chain[-1]

    def full_chain(self):
        """ Metodo responsavel por retornar toda a chain e o tamanho dela """
        return self.chain, len(self.chain)

    @ staticmethod
    def hash(block):
        """ Metodo responsavel por criar o hash do bloco """
        block_str = json.dumps(block, sort_keys=True).encode()  # obj -> string
        return hashlib.sha256(block_str).hexdigest()
