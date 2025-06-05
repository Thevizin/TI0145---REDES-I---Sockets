def set_decryption_algorithm(algorithm):
    """
    Set the decryption algorithm to be used.
    """
    global decryption_algorithm
    decryption_algorithm = algorithm

def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message using the specified key.
    
    Parameters:
    encrypted_message (bytes): The message to decrypt.
    key (bytes): The key to use for decryption.
    
    Returns:
    str: The decrypted message.
    """
    if decryption_algorithm == 'AES':
        from Crypto.Cipher import AES
        cipher = AES.new(key, AES.MODE_EAX)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode('utf-8')
    else:
        raise ValueError("Unsupported decryption algorithm")