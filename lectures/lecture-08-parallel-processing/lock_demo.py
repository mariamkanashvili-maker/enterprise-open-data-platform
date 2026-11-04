"""
lecture 8: Race Condition და Lock — რატომ გვჭირდება threading.Lock.
"""

import threading
import time

ITERATIONS = 2_000
THREAD_COUNT = 4


def increment_unsafe(counter: list) -> None:
    for _ in range(ITERATIONS):
        current = counter[0]
        time.sleep(0)  # ხელოვნურად ვაიძულებთ thread switch-ს race condition-ის საჩვენებლად
        counter[0] = current + 1


def increment_safe(counter: list, lock: threading.Lock) -> None:
    for _ in range(ITERATIONS):
        with lock:
            current = counter[0]
            time.sleep(0)
            counter[0] = current + 1


def run(target, *args) -> int:
    counter = [0]
    threads = [threading.Thread(target=target, args=(counter, *args)) for _ in range(THREAD_COUNT)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter[0]


def main() -> None:
    expected = ITERATIONS * THREAD_COUNT

    unsafe_result = run(increment_unsafe)
    status = "[OK]" if unsafe_result == expected else f"[FAIL] დაკარგულია {expected - unsafe_result} ინკრემენტი"
    print(f"Lock-ის გარეშე: {unsafe_result:,} (მოსალოდნელი: {expected:,}) {status}")

    lock = threading.Lock()
    safe_result = run(increment_safe, lock)
    status = "[OK]" if safe_result == expected else "[FAIL]"
    print(f"Lock-ით: {safe_result:,} (მოსალოდნელი: {expected:,}) {status}")


if __name__ == "__main__":
    main()
