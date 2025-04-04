import sympy
import random

# Funkcja generująca losową 4-cyfrową liczbę pierwszą
def generate_large_prime():
    return sympy.randprime(1000, 9999)

# Funkcja obliczająca największy wspólny dzielnik (GCD) dwóch liczb
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Funkcja generująca klucze RSA (publiczny i prywatny)
def generate_keys():
    p = generate_large_prime()  # Pierwsza liczba pierwsza
    q = generate_large_prime()  # Druga liczba pierwsza
    while p == q:  # Zapewnienie, że p i q są różne
        q = generate_large_prime()

    n = p * q  # Moduł RSA
    phi = (p - 1) * (q - 1)  # Funkcja Eulera phi(n)

    # Wybór wykładnika publicznego e
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:  # e musi być względnie pierwsze z phi(n)
        e = random.randrange(2, phi)

    # Obliczenie odwrotności modularnej e względem phi(n) dla klucza prywatnego d
    d = pow(e, -1, phi)

    return ((e, n), (d, n))  # Zwraca klucz publiczny i prywatny

# Funkcja szyfrująca wiadomość przy użyciu klucza publicznego
def encrypt(message, public_key):
    e, n = public_key  # Pobranie wartości klucza publicznego
    encrypted_message = [pow(ord(char), e, n) for char in message]  # Szyfrowanie znaków ASCII
    return encrypted_message

# Funkcja deszyfrująca wiadomość przy użyciu klucza prywatnego
def decrypt(encrypted_message, private_key):
    d, n = private_key  # Pobranie wartości klucza prywatnego
    decrypted_message = ''.join(chr(pow(char, d, n)) for char in encrypted_message)  # Odszyfrowanie znaków
    return decrypted_message

if __name__ == "__main__":
    public_key, private_key = generate_keys()  # Generowanie kluczy RSA

    message = "WITAM, Z TEJ STRONY RSA!"  # Wiadomość do zaszyfrowania
    encrypted_msg = encrypt(message, public_key)  # Szyfrowanie wiadomości
    decrypted_msg = decrypt(encrypted_msg, private_key)  # Deszyfrowanie wiadomości

    # Wyświetlenie wyników
    print("Public Key:", public_key)
    print("Private Key:", private_key)
    print("Original Message:", message)
    print("Encrypted Message:", encrypted_msg)
    print("Decrypted Message:", decrypted_msg)
