import random
import sympy


def generate_prime():
    """
    Generuje losową liczbę pierwszą p, spełniającą warunek p ≡ 3 (mod 4),
    co jest wymagane dla poprawnego działania generatora Blum-Blum-Shub (BBS).
    """
    while True:
        p = sympy.randprime(1000, 9999)  # Wybieramy losową liczbę pierwszą z zakresu 4 cyfr
        if p % 4 == 3:  # Musi spełniać warunek p ≡ 3 (mod 4)
            return p


def generate_bbs_sequence(length):
    """
    Generuje sekwencję bitów o podanej długości przy użyciu generatora BBS.
    """
    p, q = generate_prime(), generate_prime()  # Dwie różne liczby pierwsze
    N = p * q  # Obliczamy N = p × q

    x = random.randint(2, N - 1)  # Wybieramy losowe x < N
    while sympy.gcd(x, N) != 1:  # x musi być względnie pierwsze z N
        x = random.randint(2, N - 1)

    x = (x ** 2) % N  #  początkowy stan generatora
    sequence = []
    for _ in range(length):  # Generujemy kolejne bity
        x = (x ** 2) % N  # mod N
        sequence.append(x % 2)  # Pobieramy najmniej znaczący bit (LSB)

    return sequence


def monobit_test(sequence):
    """
    Test monobitowy: sprawdza, czy liczba jedynek i zer w sekwencji
    """
    ones = sum(sequence)  # Liczba jedynek
    return 9725 <= ones <= 10275  # Sprawdzamy czy mieści się w przedziale


def long_run_test(sequence):
    """
    Test długiej serii: sprawdza, czy w sekwencji nie występuje
    zbyt długa seria powtarzających się bitów.
    """
    max_run = 0
    current_run = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:  # Jeśli to ten sam bit co poprzedni
            current_run += 1
        else:
            max_run = max(max_run, current_run)  # Zapisujemy największą dotychczasową serię
            current_run = 1
    max_run = max(max_run, current_run)  # Ostateczna największa seria

    return max_run < 26  # Maksymalna długość serii < 26


def runs_test(sequence):
    """
    Test serii: sprawdza, czy liczba serii o różnej długości
    mieści się w oczekiwanym przedziale.
    """
    counts = {i: 0 for i in range(1, 7)}  # Liczymy serie długości 1-6+
    current_run = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:  # Jeśli seria trwa
            current_run += 1
        else:
            counts[min(current_run, 6)] += 1  # Liczymy serię (maks. 6)
            current_run = 1
    counts[min(current_run, 6)] += 1  # Ostatnia seria
    print(counts)
    return (2315 <= counts[1]/2 <= 2685 and
            1114 <= counts[2]/2 <= 1386 and
            527 <= counts[3]/2 <= 723 and
            240 <= counts[4]/2 <= 384 and
            103 <= counts[5]/2 <= 209 and
            103 <= counts[6]/2 <= 209)


def poker_test(sequence):
    """
    Test pokera: dzieli ciąg bitów na grupy po 4 bity,
    sprawdza ich częstość i oblicza wartość statystyki X^2.
    """
    m = 4  # Dzielimy ciąg na grupy po 4 bity
    k = len(sequence) // m
    groups = [tuple(sequence[i * m:(i + 1) * m]) for i in range(k)]

    freq = {}  # Liczność wystąpień każdej grupy
    for g in groups:
        freq[g] = freq.get(g, 0) + 1

    x = (16 / k) * sum(f ** 2 for f in freq.values()) - k
    return 2.16 <= x <= 46.17  # Musi być w przedziale


if __name__ == "__main__":
    """
    Generuje 20 000 bitów przy użyciu BBS i wykonuje 4 testy losowości.
    """
    seq = generate_bbs_sequence(20000)
    print("Monobit test:", monobit_test(seq))
    print("Long run test:", long_run_test(seq))
    print("Runs test:", runs_test(seq))
    print("Poker test:", poker_test(seq))