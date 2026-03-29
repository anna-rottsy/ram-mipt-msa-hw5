import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import time


def get_clean_words(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Получаем текст страницы
    text = soup.get_text().lower()

    # Оставляем только слова
    words = re.findall(r'\b\w+\b', text)

    return words


def load_words(file_path):
    with open(file_path, 'r') as file:
        # Убираем дубликаты + приводим к нижнему регистру
        return list(set(
            line.strip().lower()
            for line in file if line.strip()
        ))


def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    start_time = time.time()

    # Загружаем слова из файла
    words_to_count = load_words(words_file)

    # Загружаем текст сайта ОДИН раз
    words = get_clean_words(url)

    # Считаем частоты за один проход
    counter = Counter(words)

    # Формируем результат
    frequencies = {
        word: counter[word]
        for word in words_to_count
    }

    # (опционально) сортировка по частоте
    frequencies = dict(sorted(frequencies.items(), key=lambda x: -x[1]))

    end_time = time.time()

    print("Frequencies:")
    print(frequencies)
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
