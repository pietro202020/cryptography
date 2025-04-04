import hashlib
import time
import random
import matplotlib.pyplot as plt


def generate_hashes(input_text):
    hashes = {
        "MD5": hashlib.md5(input_text.encode()).hexdigest(),
        "SHA-1": hashlib.sha1(input_text.encode()).hexdigest(),
        "SHA-256": hashlib.sha256(input_text.encode()).hexdigest(),
        "SHA-512": hashlib.sha512(input_text.encode()).hexdigest(),
        "SHA3-256": hashlib.sha3_256(input_text.encode()).hexdigest(),
        "SHA3-512": hashlib.sha3_512(input_text.encode()).hexdigest()
    }
    return hashes

#Mierzy szybkość wykonania każdego algorytmu hashującego dla inputa
def measure_hash_speed(input_text, iterations=10000):
    results = {}
    algos = {
        "md5": "MD5",
        "sha1": "SHA-1",
        "sha256": "SHA-256",
        "sha512": "SHA-512",
        "sha3_256": "SHA3-256",
        "sha3_512": "SHA3-512"
    }

    for algo, display_name in algos.items():
        start_time = time.time()
        for _ in range(iterations):
            hashlib.new(algo, input_text.encode()).hexdigest()
        elapsed_time = time.time() - start_time
        results[display_name] = elapsed_time
    return results


def measure_speed_vs_size(sizes, iterations=1000):
    results = {
        "MD5": [],
        "SHA-1": [],
        "SHA-256": [],
        "SHA-512": [],
        "SHA3-256": [],
        "SHA3-512": []
    }

    # Mapowanie między nazwami algorytmów a kluczami w słowniku wyników
    algo_mapping = {
        "md5": "MD5",
        "sha1": "SHA-1",
        "sha256": "SHA-256",
        "sha512": "SHA-512",
        "sha3_256": "SHA3-256",
        "sha3_512": "SHA3-512"
    }

    for size in sizes:
        input_text = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=size))
        for algo, key in algo_mapping.items():
            start_time = time.time()
            for _ in range(iterations):
                hashlib.new(algo, input_text.encode()).hexdigest()
            elapsed_time = time.time() - start_time
            results[key].append(elapsed_time)
    return results


def plot_hash_speeds_vs_size(size_results, sizes):
    # Konwersja rozmiarów z bajtów na megabajty (1MB = 1 000 000 bajtów)
    sizes_mb = [size / 1000000 for size in sizes]

    plt.figure(figsize=(10, 6))
    for algo, times in size_results.items():
        plt.plot(sizes_mb, times, marker='o', label=algo)
    plt.xlabel("Rozmiar wejścia (MB)")
    plt.ylabel("Czas obliczeń (s)")
    plt.title("Porównanie szybkości funkcji hashujących względem rozmiaru wejścia")
    plt.legend()
    plt.grid()
    plt.show()


def find_collisions(hash_function, num_tests=100000, bits=12):
    seen = {}
    for _ in range(num_tests):
        test_input = str(random.randint(0, 10 ** 10))
        hash_value = hashlib.new(hash_function, test_input.encode()).hexdigest()
        truncated_hash = hash_value[:bits // 4]  # 12 bitów = 3 heksadecymalne znaki
        if truncated_hash in seen:
            return test_input, seen[truncated_hash], truncated_hash  # Znaleziono kolizję
        seen[truncated_hash] = test_input
    return None


def strict_avalanche_criteria(hash_function, input_text):
    original_hash = hashlib.new(hash_function, input_text.encode()).hexdigest()
    flipped_bit = list(input_text)
    flipped_bit[0] = '1' if flipped_bit[0] == '0' else '0'  # Zmieniamy jeden bit
    flipped_text = "".join(flipped_bit)
    new_hash = hashlib.new(hash_function, flipped_text.encode()).hexdigest()

    changes = sum(1 for a, b in zip(original_hash, new_hash) if a != b)
    total_bits = len(original_hash) * 4  # Każdy znak hexa to 4 bity
    probability = changes / total_bits

    return probability


def main():
    user_input = input("Podaj tekst do zahashowania: ")

    print("Wygenerowane hashe:")
    hashes = generate_hashes(user_input)
    for algo, hash_value in hashes.items():
        print(f"{algo}: {hash_value}")

    print("\nPorównanie szybkości działania funkcji hashujących:")
    speeds = measure_hash_speed(user_input)
    for algo, time_taken in speeds.items():
        print(f"{algo}: {time_taken:.4f} s")

    print("\nSzukamy kolizji na pierwszych 12 bitach w SHA-256...")
    collision = find_collisions("sha256")
    if collision:
        print(f"Kolizja znaleziona! Teksty: {collision[0]} i {collision[1]}, hash: {collision[2]}")
    else:
        print("Brak kolizji po przetestowaniu 100 000 wartości.")

    print("\nTest losowości (Strict Avalanche Criteria) dla SHA-256:")
    avalanche_score = strict_avalanche_criteria("sha256", user_input)
    print(f"Procent zmienionych bitów: {avalanche_score * 100:.2f}%")

    generate_plots = input("\nCzy chcesz wygenerować wykresy porównujące szybkość algorytmów? (tak/nie): ").lower()
    if generate_plots == "tak":
        sizes = [1, 1000000, 5000000, 10000000]  # Różne rozmiary wejścia
        print("\nMierzenie czasu w zależności od rozmiaru wejścia...")
        size_results = measure_speed_vs_size(sizes)
        plot_hash_speeds_vs_size(size_results, sizes)


if __name__ == "__main__":
    main()