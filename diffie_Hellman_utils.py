import random
import hashlib

def is_prime(num):
    """
    Verifica se um número é primo.
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_random_prime(limite_inferior, limite_superior):
    """
    Gera um número primo aleatório dentro de um intervalo.
    """
    while True:
        numero_aleatorio = random.randint(limite_inferior, limite_superior)
        if is_prime(numero_aleatorio):
            return numero_aleatorio

def generate_private_key(prime):
    # Generate a private key that is a random integer in the range [2, prime - 2].
    if prime <= 2:
        raise ValueError("Prime must be greater than 2.")
    return random.randint(2, prime - 2)

def generate_public_key(private_key, base, prime):
    # Generate a public key using the private key, base, and prime.
    return pow(base, private_key, prime)

def generate_keys():
    """
    Gera um par de chaves (pública e privada) para o algoritmo Diffie-Hellman.
    """
    lim_inf = 1000
    lim_sup = 10000
    prime = generate_random_prime(lim_inf, lim_sup)
    base = random.randint(2, prime - 1)
    private_key = generate_private_key(prime)
    public_key = generate_public_key(private_key, base, prime)
    return public_key, private_key

def compute_shared_secret(public_key, private_key, prime):
    # Compute the shared secret using the public key, private key, and prime.
    if public_key <= 0 or private_key <= 0 or prime <= 0:
        raise ValueError("Public key, private key, and prime must be positive integers.")
    return pow(public_key, private_key, prime)

def hash_shared_secret(shared_secret):
    # Hash the shared secret using SHA-256.
    if shared_secret <= 0:
        raise ValueError("Shared secret must be a positive integer.")
    return hashlib.sha256(str(shared_secret).encode()).hexdigest()