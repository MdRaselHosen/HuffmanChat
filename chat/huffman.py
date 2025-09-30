import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node:
        if node.char is not None:
            code_map[node.char] = prefix
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(text):
    if not text:
        return "", {}, 0, 0
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    encoded_text = ''.join(codes[ch] for ch in text)
    original_size = len(text.encode('utf-8')) * 8
    compressed_size = len(encoded_text)
    return encoded_text, codes, original_size, compressed_size

def huffman_decode(encoded_text, codes):
    reverse_map = {v: k for k, v in codes.items()}
    decoded_text = ""
    buffer = ""
    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_map:
            decoded_text += reverse_map[buffer]
            buffer = ""
    return decoded_text



text = "Hello, This is Md. Rasel Hosen"

encoded_text,codes,original_size,compressed_size = huffman_encode(text)
print(encoded_text)
print("------------------------------------")
print(codes)
print("------------------------------------")
print("original size is" ,original_size, "compressed size is ", compressed_size)
print("------------------------------------")

decode = huffman_decode(encoded_text, codes)
print(decode)
