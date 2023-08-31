import time
import rail_fence
import rail_fence2
import multiprocess

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


example_cipher = "dme  udtgceonhe i nbdt eniTI emh lpeitos san o hgnnit,i s   t eathjcnniundisse o tttpo nh naeaoenstN.    eei.xlslap lma"

start = time.time()
wordlist = load_word_list("common_words.txt")
end = time.time()
print(f"load wordlist: \tTime taken: {(end-start):.04f}s")

start = time.time_ns()
results = rail_fence2.brute_force_rf(example_cipher, wordlist)
end = time.time_ns()
# show time of execution per iteration
print(f"Std functions: \tTime taken: {((end-start) / 1000000):.04f}ms")
sorted_list = sorted(results, key=results.get, reverse=True)
print(f" key:{sorted_list[0][0]}  offset:{sorted_list[0][1]}")

start = time.time_ns()
results = rail_fence.brute_force_rf(example_cipher, wordlist)
end = time.time_ns()
# show time of execution per iteration
print(f"Recursion: \tTime taken: {((end-start) / 1000000):.04f}ms")
sorted_list = sorted(results, key=results.get, reverse=True)
print(f" key:{sorted_list[0][0]}  offset:{sorted_list[0][1]}")
'''
start = time.time()
results = multiprocess.brute_force_rf(example_cipher, wordlist)
end = time.time()
# show time of execution per iteration
print(f"Multiprocess: \tTime taken: {(end-start):.04f}s")
sorted_list = sorted(results, key=results.get, reverse=True)
print(f" key:{sorted_list[0][0]}  offset:{sorted_list[0][1]}")
'''