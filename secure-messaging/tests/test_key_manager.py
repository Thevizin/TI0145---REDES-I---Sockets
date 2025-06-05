import unittest
from src.utils.key_manager import add_key, remove_key, get_key

class TestKeyManager(unittest.TestCase):

    def setUp(self):
        self.test_key = "test_key"
        self.test_key_value = "test_value"
        add_key(self.test_key, self.test_key_value)

    def tearDown(self):
        remove_key(self.test_key)

    def test_add_key(self):
        result = get_key(self.test_key)
        self.assertEqual(result, self.test_key_value)

    def test_remove_key(self):
        remove_key(self.test_key)
        result = get_key(self.test_key)
        self.assertIsNone(result)

    def test_get_key_non_existent(self):
        result = get_key("non_existent_key")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()