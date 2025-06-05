import unittest
from src.crypto.decryption import decrypt_message, set_decryption_algorithm
from src.crypto.keys import load_key

class TestDecryption(unittest.TestCase):

    def setUp(self):
        self.key = load_key("keys/private/private_key.pem")
        self.algorithm = set_decryption_algorithm("AES")
        self.encrypted_message = b"..."  # Replace with actual encrypted message

    def test_decrypt_message(self):
        decrypted_message = decrypt_message(self.encrypted_message, self.key)
        self.assertEqual(decrypted_message, "Expected decrypted message")  # Replace with expected message

    def test_decrypt_invalid_message(self):
        with self.assertRaises(ValueError):
            decrypt_message(b"invalid_encrypted_data", self.key)

if __name__ == '__main__':
    unittest.main()