import unittest

from ai.default_args.lstm import get_lstm_default


class TestDemo(unittest.TestCase):

    def test_hello_world(self):
        print(f"hello world!")

    def test_lstm_default(self):
        args = get_lstm_default()
        print(args)
