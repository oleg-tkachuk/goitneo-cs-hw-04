import os
import pprint as pp
from time import time
from multiprocessing import Pool, Manager, cpu_count

keywords = ['cat', 'dog', 'test', 'git', 'python', 'example', 'blah-blah-blah']


def find_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def search_keywords(keywords, file_path, queue):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    queue.put((keyword, file_path))
    except Exception as e:
        print(f"[error] Error reading file {file_path}: {e}")


def main(keywords, directory):
    start_time = time()

    files = find_files(directory)

    with Manager() as manager:
        queue = manager.Queue()
        results = {}

        with Pool(processes=cpu_count()) as pool:
            for file_path in files:
                pool.apply_async(search_keywords, args=(
                    keywords, file_path, queue))

            pool.close()
            pool.join()

            while not queue.empty():
                keyword, path = queue.get()
                if keyword in results:
                    results[keyword].append(path)
                else:
                    results[keyword] = [path]

        end_time = time()
        print(f"[info] Total execution time: {
              end_time - start_time} seconds\n")

        return results


if __name__ == "__main__":
    pp.pprint(main(keywords=keywords, directory='.'))
