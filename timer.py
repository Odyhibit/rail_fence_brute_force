import time
import os
import rail_fence
import rail_fence2

def load_word_list(path: str) -> []:
    """Returns a list of words in the file with the longest first."""
    with open(path, "r") as common_words:
        common_word_list = []
        while line := common_words.readline():
            common_word_list.append(line.strip())
        return sorted(common_word_list, key=len, reverse=True)

def decode_rf(cipher: str, key: int, offset: int = 0) -> str:
    period = 2 * key - 2
    plaintext = ["_"] * len(cipher)
    index = 0
    for row in range(key):
        for i in range(len(cipher)):
            if (i + offset) % period == row or period - ((i + offset) % period) == row:
                plaintext[i] = cipher[index]
                index += 1
    return "".join(plaintext)

wordlist = load_word_list("common_words.txt")
example_cipher = "T j epse tneo gnhilNo sd hmninhsi uta xml etneta  eddt eln,adta sal opiti pnigmc ieo hsoeissnaenchIe bo  t . nnenut t ."


start = time.time()
rail_fence2.brute_force_rf(example_cipher, wordlist)
end = time.time()
# show time of execution per iteration
print(f"Std functions: \tTime taken: {(end-start)*10**3:.03f}ms")

start = time.time()
rail_fence.brute_force_rf(example_cipher, wordlist)
end = time.time()
# show time of execution per iteration
print(f"Recursion: \tTime taken: {(end-start)*10**3:.03f}ms")

