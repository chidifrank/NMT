import unittest

from src.components.util.call_model import call_model


class IntegrationTests(unittest.TestCase):

    def test_if_model_works(self):
        self.assertEqual(call_model(), 0)


if __name__ == '__main__':
    unittest.main()
