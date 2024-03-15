import os
import threading
from time import time
import pprint as pp
from collections import defaultdict

keywords = ['cat', 'dog', 'test', 'git', 'python', 'example', 'blah-blah-blah']


def find_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def search_keywords(keywords, file_path, results):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    results[keyword].append(file_path)

    except Exception as e:
        print(f"[error] Error reading file {file_path}: {e}")


def thread_function(keywords, file_paths, results):
    for file_path in file_paths:
        search_keywords(keywords, file_path, results)


def main(keywords, num_threads=5):

    start_time = time()

    files = find_files('.')

    results = defaultdict(list)

    files_per_thread = len(files) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * files_per_thread
        end = None if i == num_threads - 1 else (i + 1) * files_per_thread
        thread = threading.Thread(
            target=thread_function, args=(keywords, files[start:end], results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time()
    print(f"[info] Total execution time: {end_time - start_time} seconds\n")

    return dict(results)


if __name__ == "__main__":
    pp.pprint(main(keywords=keywords, num_threads=10))
