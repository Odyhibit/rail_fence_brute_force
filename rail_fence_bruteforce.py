import click


@click.command()
@click.option('-t', '--cipher-text', help='The ciphered text enclosed in quotes.')
def main(cipher_text):
    green = "\u001b[32m"
    reset = "\u001b[0m"
    cipher_text = cipher_text
    if cipher_text is None:
        print("Nothing to solve, please give me some cipher text.")
        return
    common_words_longest_first = load_word_list("common_words.txt")
    # print(common_words_longest_first)
    row, offset, count_dict = brute_force(cipher_text, common_words_longest_first)

    print(f"Using key:{green}{row}{reset} offset:{green}{offset}{reset} I found {count_dict[(row, offset)]} words")
    print("Decoding with most likely settings . . .")
    print()

    sorted_list = sorted(count_dict, key=count_dict.get, reverse=True)
    # print(count_dict)
    # print(sorted_list)
    sorted_list.pop(0)
    keep_going = True
    while keep_going:
        print(decode(cipher_text, row, offset))
        print()
        response = input(f"Does that look correct ({green}y{reset}/{green}n{reset})")
        if response == "n" or response == "N":
            row, offset = sorted_list.pop(0)
            print(f"key:{row} offset:{offset} words found {count_dict[(row, offset)]}")
        if response == "y" or response == "Y":
            keep_going = False


def decode(cipher: str, key: int, offset: int = 0) -> str:
    period = 2 * key - 2
    plaintext = ["_"] * len(cipher)
    index = 0
    for row in range(key):
        for i in range(len(cipher)):
            if (i + offset) % period == row or period - ((i + offset) % period) == row:
                plaintext[i] = cipher[index]
                index += 1
    return "".join(plaintext)


def brute_force(cipher: str, wordlist: []):
    cipher = cipher.lower()
    word_count_dictionary = {}
    highest_word_count = 0
    row_candidate = 0
    offset_candidate = 0
    highest_row_to_try = len(cipher) // 2 + 4
    print(f"Trying row values 2-{highest_row_to_try} using all possible offsets")
    for key in range(2, highest_row_to_try):
        period = 2 * (key - 1)
        for offset in range(period):
            word_count = 0
            candidate = decode(cipher, key, offset)
            for word in wordlist:
                word_occurrences, candidate = count_and_remove(word, candidate)
                word_count += word_occurrences
            if word_count > highest_word_count:
                highest_word_count = word_count
                row_candidate = key
                offset_candidate = offset
            word_count_dictionary[(key, offset)] = word_count
    return row_candidate, offset_candidate, word_count_dictionary


def count_and_remove(needle: str, haystack: str, current_count: int = 0) -> (int, str):
    index = haystack.find(needle)
    if index == -1:
        return current_count, haystack
    new_haystack = haystack[:index] + haystack[index + len(needle):]
    current_count += 1
    return count_and_remove(needle, new_haystack, current_count)


def load_word_list(path: str) -> []:
    with open(path, "r") as common_words:
        common_word_list = []
        while line := common_words.readline():
            common_word_list.append(line.strip())
        return sorted(common_word_list, key=len, reverse=True)


if __name__ == "__main__":
    main()
