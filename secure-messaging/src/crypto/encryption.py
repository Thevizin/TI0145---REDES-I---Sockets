def set_encryption_algorithm(algorithm):
    """
    Set the encryption algorithm to be used.
    Supported algorithms: 'AES', 'RSA', etc.
    """
    global encryption_algorithm
    encryption_algorithm = algorithm

def encrypt_message(message, key):
    """
    Encrypts a message using the specified key and the current encryption algorithm.
    
    Parameters:
    - message (str): The message to encrypt.
    - key (bytes): The key to use for encryption.
    
    Returns:
    - bytes: The encrypted message.
    """
    if encryption_algorithm == 'AES':
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        import os
        
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ct_bytes  # Prepend IV for decryption

    elif encryption_algorithm == 'RSA':
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_OAEP
        
        rsa_key = RSA.import_key(key)
        cipher = PKCS1_OAEP.new(rsa_key)
        return cipher.encrypt(message.encode())

    else:
        raise ValueError("Unsupported encryption algorithm")

# Initialize the default encryption algorithm
encryption_algorithm = 'AES'  # Default to AES encryption