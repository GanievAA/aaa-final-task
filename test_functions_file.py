import unittest
from telegram_bot import won


class TestWonFunc(unittest.TestCase):

    def setUp(self):
        self.won = won

    def test_first_row_for_crosses(self):
        self.assertEqual(self.won(['X', 'X', 'X', '.', '.', '.', '.', '.', '.']), True)

    def test_second_row_for_crosses(self):
        self.assertEqual(self.won(['.', '.', '.', 'X', 'X', 'X', '.', '.', '.']), True)

    def test_third_row_for_crosses(self):
        self.assertEqual(self.won(['.', '.', '.', '.', '.', '.', 'X', 'X', 'X']), True)

    def test_first_column_for_crosses(self):
        self.assertEqual(self.won(['X', '.', '.', 'X', '.', '.', 'X', '.', '.']), True)

    def test_second_column_for_crosses(self):
        self.assertEqual(self.won(['.', 'X', '.', '.', 'X', '.', '.', 'X', '.']), True)

    def test_third_column_for_crosses(self):
        self.assertEqual(self.won(['.', '.', 'X', '.', '.', 'X', '.', '.', 'X']), True)

    def test_pos_diagonal_for_crosses(self):
        self.assertEqual(self.won(['X', '.', '.', '.', 'X', '.', '.', '.', 'X']), True)

    def test_neg_diagonal_for_crosses(self):
        self.assertEqual(self.won(['.', '.', 'X', '.', 'X', '.', 'X', '.', '.']), True)

    def test_first_row_for_zeros(self):
        self.assertEqual(self.won(['0', '0', '0', '.', '.', '.', '.', '.', '.']), True)

    def test_second_row_for_zeros(self):
        self.assertEqual(self.won(['.', '.', '.', '0', '0', '0', '.', '.', '.']), True)

    def test_third_row_for_zeros(self):
        self.assertEqual(self.won(['.', '.', '.', '.', '.', '.', '0', '0', '0']), True)

    def test_first_column_for_zeros(self):
        self.assertEqual(self.won(['0', '.', '.', '0', '.', '.', '0', '.', '.']), True)

    def test_second_column_for_zeros(self):
        self.assertEqual(self.won(['.', '0', '.', '.', '0', '.', '.', '0', '.']), True)

    def test_third_column_for_zeros(self):
        self.assertEqual(self.won(['.', '.', '0', '.', '.', '0', '.', '.', '0']), True)

    def test_pos_diagonal_for_zeros(self):
        self.assertEqual(self.won(['0', '.', '.', '.', '0', '.', '.', '.', '0']), True)

    def test_neg_diagonal_for_zeros(self):
        self.assertEqual(self.won(['.', '.', '0', '.', '0', '.', '0', '.', '.']), True)


if __name__ == "__main__":
    unittest.main()
