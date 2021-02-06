from flask import request, Flask
import unittest
from recebimento import BlockChain, app
from categorias import Categoria
import json

client = app.test_client()


class TestBlockChain(unittest.TestCase):

    def test_last(self):
        last_hash = 123

        r = client.get('http://localhost:5000/last')
        data = json.loads(r.data)
        last_api = data[0]
        self.assertEqual(
            last_hash, last_api['previous_hash'])
        # self.assertEqual(
        #     last_guaranteed['previous_hash'], last_api['previous_hash'])

    def test_transaction(self):
        payload = {'categoria': Categoria.ENTRADA.value,
                   'notas': ['132', '465'], 'empresa': 'Unilever'}
        r = client.get('/transaction/new', json=payload)
        data = json.loads(r.data)
        transaction_api = data[0]['transaction']
        self.assertEqual(
            transaction_api['empresa'], 'Unilever')

    def test_mining(self):
        r = client.get('http://localhost:5000/last')
        data = json.loads(r.data)
        print(data)

        payload = {'categoria': Categoria.ENTRADA.value,
                   'notas': ['132', '465'], 'empresa': 'Unilever'}
        r = client.get('/transaction/new', json=payload)
        payload = {'categoria': Categoria.SAIDA.value,
                   'notas': ['457', '987'], 'empresa': 'Ambev'}
        r = client.get('/transaction/new', json=payload)

        r = client.get('/mining')

        r = client.get('http://localhost:5000/last')
        data = json.loads(r.data)
        print(data)
        last_api = data[0]

        # Metodo de analise off-chain em cima do last_api lido

        transactions = last_api['transactions']

        self.assertEqual(transactions[1]['empresa'], 'Ambev')

    # def test_newNode():


if __name__ == '__main__':
    unittest.main()
