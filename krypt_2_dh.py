import random
import sympy


def find_primitive_root(p):
    for g in range(2, p):
        seen = set()
        for x in range(1, p):
            seen.add(pow(g, x, p))
        if len(seen) == p - 1:
            return g
    return None


def diffie_hellman():
    # 1. Wybór dużej liczby pierwszej n
    n = sympy.randprime(1000, 9999)  # Duża liczba pierwsza
    g = find_primitive_root(n)  # Pierwiastek pierwotny modulo n

    # 2. A wybiera klucz prywatny x i oblicza X
    x = random.randint(2, n - 2)  # Klucz prywatny A
    X = pow(g, x, n)  # Klucz publiczny A

    # 3. B wybiera klucz prywatny y i oblicza Y
    y = random.randint(2, n - 2)  # Klucz prywatny B
    Y = pow(g, y, n)  # Klucz publiczny B

    # 4. Wymiana kluczy publicznych między A i B

    # 5. Obliczenie wspólnego klucza
    key_A = pow(Y, x, n)  # Oblicza klucz sesji na podstawie Y od B
    key_B = pow(X, y, n)  # Oblicza klucz sesji na podstawie X od A

    return {
        "n": n, "g": g,
        "A_private": x, "A_public": X,
        "B_private": y, "B_public": Y,
        "Key_A": key_A, "Key_B": key_B
    }


if __name__ == "__main__":
    keys = diffie_hellman()
    print("Liczba pierwsza n:", keys["n"])
    print("Pierwiastek pierwotny g:", keys["g"])
    print("Klucz prywatny A:", keys["A_private"], "| Klucz publiczny A:", keys["A_public"])
    print("Klucz prywatny B:", keys["B_private"], "| Klucz publiczny B:", keys["B_public"])
    print("Wspólny klucz obliczony przez A:", keys["Key_A"])
    print("Wspólny klucz obliczony przez B:", keys["Key_B"])
    print("Czy klucze są równe?", keys["Key_A"] == keys["Key_B"])
