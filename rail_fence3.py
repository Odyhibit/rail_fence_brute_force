import concurrent.futures


def print_all(sorted_most_likely: [], cipher_text: str):
    for (row, offset) in sorted_most_likely:
        print(decode_rf(cipher_text, row, offset))
    return


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


def process_test_values(cipher: str, key: int, offset: int, wordlist: []):
    plain_text = decode_rf(cipher, key, offset)
    letter_count = 0
    for word in wordlist:
        letter_count += count_and_remove(word, plain_text)
    return letter_count


def brute_force_rf(cipher: str, wordlist: []):
    cipher = cipher.lower()
    possibilities = []
    word_count_dictionary = {}
    highest_row_to_try = len(cipher) // 2 + 4
    print(f"Trying row values 2-{highest_row_to_try} using all possible offsets")
    for key in range(2, highest_row_to_try):
        period = 2 * (key - 1)
        for offset in range(period):
            possibilities.append((key, offset))
            #letter_count = process_test_values(cipher, key, offset, wordlist)
            #word_count_dictionary[(key, offset)] = letter_count
    print(f"possibilities: {len(possibilities)}")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_test_values, cipher, possibilities[0], possibilities[1], wordlist)
        for (key, offset), letter_count in zip(possibilities, results):
            word_count_dictionary[(key, offset)] = letter_count
    return word_count_dictionary


def count_and_remove(needle: str, haystack: str) -> (int, str):
    """recursively removes the word and then looks again keeping a count
       Returns: count of how many times the word occurred, and the text with the word removed
    """
    num_found = haystack.count(needle)
    letter_count = len(needle) * num_found
    return letter_count


def load_word_list(path: str) -> []:
    """Returns a list of words in the file with the longest first."""
    with open(path, "r") as common_words:
        common_word_list = []
        while line := common_words.readline():
            common_word_list.append(line.strip())
        return sorted(common_word_list, key=len, reverse=True)


def encode(plaintext: str, key: int, offset: int) -> str:
    period = 2 * key - 2
    rows = [[] for _ in range(key)]
    for i, char in enumerate(plaintext):
        row_index = key - 1 - abs(period // 2 - (i + offset) % period)
        rows[row_index] += plaintext[i]
    return ''.join(str(item) for inner_list in rows for item in inner_list)


def main():
    test_val = "dme  udtgceonhe i nbdt eniTI emh lpeitos san o hgnnit,i s   t eathjcnniundisse o tttpo nh naeaoenstN.    eei.xlslap lma"
    mydict = brute_force_rf(test_val, load_word_list("common_words.txt"))
    print(mydict)
    '''
    flags = build_flag(three_letters)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(flags, executor.map(check_password, flags)):
            print('%d is prime: %s' % (number, prime))
    '''


if __name__ == '__main__':
    main()
