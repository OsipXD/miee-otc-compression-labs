from collections import Counter


def frequency_counter(filename):
    counter = Counter()
    file_size = 0
    with open(filename, 'rb') as f:
        for char in iter(lambda: f.read(1), b''):
            counter.update([ord(char)])
            file_size += 1
    return sorted([(code, round(quantity / file_size, 4))
                   for code, quantity in counter.items()],
                  key=lambda x: x[1], reverse=True)
