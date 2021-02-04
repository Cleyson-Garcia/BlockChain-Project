import unittest
from recebimento import BlockChain
from categorias import Categoria


class TestBlockChain(unittest.TestCase):

    def test_init(self):
        blockChain = BlockChain()
        self.assertEqual(blockChain.blocks()[0].get('previous_hash'), 123)

    def test_transaction(self):
        blockChain = BlockChain()
        blockChain.new_transaction(
            categoria=Categoria.ENTRADA, empresa='Unilever', notas=['123', '497'])
        self.assertTrue(blockChain.transactions())

    def test_novo_bloco(self):
        blockChain = BlockChain()
        blockChain.new_transaction(
            categoria=Categoria.ENTRADA, empresa='Ambev', notas=['7852', '78914'])
        blockChain.new_transaction(
            categoria=Categoria.ENTRADA, empresa='Unilever', notas=['123', '497'])

        blockChain.new_block(proof=15)

        self.assertEqual(blockChain.full_chain()[1], 2)
        self.assertFalse(blockChain.pending_transactions())

        blockChain.new_transaction(
            categoria=Categoria.SAIDA, empresa='Spal', notas=['0', '897'])

        print(blockChain.transactions())
        print(blockChain.pending_transactions())
        print(blockChain.full_transactions())


if __name__ == '__main__':
    unittest.main()
