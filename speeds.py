import hashlib
import time
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
    # Poprawione nazwy kluczy, zgodne z tymi w generate_hashes
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
        input_text = "a" * size
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


def main():
    user_input = "test123"

    print("Wygenerowane hashe:")
    hashes = generate_hashes(user_input)
    for algo, hash_value in hashes.items():
        print(f"{algo}: {hash_value}")

    print("\nPorównanie szybkości działania funkcji hashujących:")
    speeds = measure_hash_speed(user_input)
    for algo, time_taken in speeds.items():
        print(f"{algo}: {time_taken:.4f} s")

    sizes = [1, 1000000, 5000000, 10000000]  # Różne rozmiary wejścia
    print("\nMierzenie czasu w zależności od rozmiaru wejścia...")
    size_results = measure_speed_vs_size(sizes)
    plot_hash_speeds_vs_size(size_results, sizes)


if __name__ == "__main__":
    main()