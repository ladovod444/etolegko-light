#!/usr/bin/env python3
"""
Скрипт для замера скорости интернета через последовательные HTTP-запросы.
"""

import sys
import time
import requests

NUM_REQUESTS = 10
TIMEOUT = 60  # секунд на один запрос

# Стандартный User-Agent, чтобы серверы не блокировали запрос как "бота"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def test_speed(url: str) -> None:
    """Делает NUM_REQUESTS последовательных GET-запросов и печатает статистику."""
    print(f"URL: {url}")
    print(f"Количество запросов: {NUM_REQUESTS}\n")

    total_time = 0.0
    total_bytes = 0

    for i in range(1, NUM_REQUESTS + 1):
        start = time.perf_counter()
        try:
            response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
            response.raise_for_status()
            data = response.content
        except requests.RequestException as e:
            print(f"Ошибка на запросе {i}: {e}")
            sys.exit(1)

        elapsed = time.perf_counter() - start
        size = len(data)

        total_time += elapsed
        total_bytes += size
        print(f"  [{i:2d}/{NUM_REQUESTS}]  {elapsed:6.3f} с  |  {size:>12} байт")

    avg_time = total_time / NUM_REQUESTS
    total_mb = total_bytes / (1024 * 1024)
    # 1 Мбит/с = 1_000_000 бит / 1 с
    speed_mbps = (total_bytes * 8) / (total_time * 1_000_000) if total_time > 0 else 0.0

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 50)
    print(f"Общее время:          {total_time:.3f} с")
    print(f"Среднее время:        {avg_time:.3f} с")
    print(f"Скачано всего:        {total_mb:.2f} МБ ({total_bytes} байт)")
    print(f"Скорость скачивания:  {speed_mbps:.2f} Мбит/с")
    print("=" * 50)


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование: python speed_test.py <URL>")
        print("Пример:       python speed_test.py https://speed.cloudflare.com/__down?bytes=10485760")
        sys.exit(1)

    test_speed(sys.argv[1])


if __name__ == "__main__":
    main()