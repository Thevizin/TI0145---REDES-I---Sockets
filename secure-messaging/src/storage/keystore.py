def save_to_keystore(key_name, key_data):
    """
    Save a cryptographic key to the keystore.
    
    Parameters:
    key_name (str): The name of the key to save.
    key_data (bytes): The key data to save.
    """
    with open(f'keys/private/{key_name}.key', 'wb') as key_file:
        key_file.write(key_data)

def load_from_keystore(key_name):
    """
    Load a cryptographic key from the keystore.
    
    Parameters:
    key_name (str): The name of the key to load.
    
    Returns:
    bytes: The key data.
    """
    try:
        with open(f'keys/private/{key_name}.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Key {key_name} not found in keystore.")
        return None