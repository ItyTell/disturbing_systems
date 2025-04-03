import numpy as np
import math
import hashlib

class BloomFilter:
    def __init__(self, expected_elements, false_positive_rate=0.01):
        # formulas from https://en.wikipedia.org/wiki/Bloom_filter
        self.size = int(-expected_elements * math.log(false_positive_rate) / (math.log(2) ** 2))
        self.hash_count = int((self.size / expected_elements) * math.log(2))

        # main thingy for the bloom filter
        self.bit_array = np.zeros(self.size, dtype=bool)

        # castom hash functions
        # we can use any hash function, but for simplicity, we'll use md5
        self.hash_functions = self._create_hash_functions(self.hash_count)

        self.elements_count = 0
    
    def _create_hash_functions(self, count):
        def _make_hash_function(seed):
            def _hash(item):
                if not isinstance(item, str):
                    item = str(item)
                value = hashlib.md5(f"{seed}:{item}".encode()).hexdigest()
                return int(value, 16) % self.size
            return _hash
        return [_make_hash_function(i) for i in range(count)]
    
    def add(self, item):
        for hash_function in self.hash_functions:
            position = hash_function(item)
            self.bit_array[position] = True
        self.elements_count += 1
    
    def contains(self, item):
        for hash_function in self.hash_functions:
            position = hash_function(item)
            if not self.bit_array[position]:
                return False
        return True
    
    def current_false_positive_rate(self):
        if self.elements_count == 0:
            return 0.0
        p = (1 - 1/self.size) ** (self.hash_count * self.elements_count)
        return (1 - p) ** self.hash_count
    
    def __contains__(self, item):
        return self.contains(item)

bloom = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
bloom.add("apple")
bloom.add("banana")
bloom.add("orange")
print("Is 'apple' in the filter?", "apple" in bloom)
print("Is 'grape' in the filter?", "grape" in bloom)
print(f"Current false positive rate: {bloom.current_false_positive_rate():.6f}")