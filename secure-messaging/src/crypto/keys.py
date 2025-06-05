def generate_key():
    """
    Generates a new cryptographic key.
    Returns:
        bytes: The generated key.
    """
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return key

def load_key(file_path):
    """
    Loads a cryptographic key from a file.
    Args:
        file_path (str): The path to the key file.
    Returns:
        PrivateKey: The loaded private key.
    """
    from cryptography.hazmat.primitives import serialization

    with open(file_path, "rb") as key_file:
        key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return key

def save_key(key, file_path):
    """
    Saves a cryptographic key to a file.
    Args:
        key (PrivateKey): The key to save.
        file_path (str): The path to the file where the key will be saved.
    """
    from cryptography.hazmat.primitives import serialization

    with open(file_path, "wb") as key_file:
        key_file.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
            )
        )