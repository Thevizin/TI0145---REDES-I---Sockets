import unittest
from src.crypto.encryption import encrypt_message, set_encryption_algorithm
from src.crypto.keys import generate_key

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.key = generate_key()
        set_encryption_algorithm('AES')  # Example algorithm

    def test_encrypt_message(self):
        message = "Hello, World!"
        encrypted_message = encrypt_message(message, self.key)
        self.assertIsNotNone(encrypted_message)
        self.assertNotEqual(message, encrypted_message)

    def test_encrypt_empty_message(self):
        message = ""
        encrypted_message = encrypt_message(message, self.key)
        self.assertIsNotNone(encrypted_message)

    def test_encrypt_with_invalid_key(self):
        with self.assertRaises(ValueError):
            encrypt_message("Hello", None)

if __name__ == '__main__':
    unittest.main()