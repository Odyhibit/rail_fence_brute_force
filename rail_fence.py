import click


@click.command()
@click.version_option(version="0.4", prog_name="rail_fence")
@click.option('-t', '--text', required=True, help='Text enclosed in quotes.')
@click.option('-k', '--key', type=int, help='The number of rows to use')
@click.option('-o', '--offset', default=0, show_default=True, type=int, help='Offset, repeats after 2(key-1)')
@click.option('--decode/--encode', '-d/-e', default=True, show_default=True)
@click.option('--brute-force', '-b', is_flag=True)
def main(text, key, offset, decode, brute_force):
    green = "\u001b[32m"
    reset = "\u001b[0m"
    cipher_text = text
    common_words_longest_first = load_word_list("common_words.txt")

    if cipher_text is None:
        print("Nothing to solve, please give me some cipher text.")
        return

    if not decode:
        print(f'Encoding With Key:{key} Offset:{offset}')
        print(encode(cipher_text, key, offset))
        print()
        return

    if decode and not brute_force:
        if key is None:
            print('Either a key or the brute-force flag are required to decode.')
            print()
            return
        else:
            print(decode_rf(text, key, offset))
            print()
            return

    # print(common_words_longest_first)
    row, offset, count_dict = brute_force_rf(cipher_text, common_words_longest_first)

    print(f"Using key:{green}{row}{reset} offset:{green}{offset}{reset} I found {count_dict[(row, offset)]} words")
    print("Decoding with most likely settings . . .")
    print()

    sorted_list = sorted(count_dict, key=count_dict.get, reverse=True)
    sorted_list.pop(0)
    keep_going = True
    while keep_going:
        print(decode_rf(cipher_text, row, offset))
        print()
        response = input(f"Does that look correct ({green}y{reset}/{green}n{reset})")
        if response == "n" or response == "N":
            row, offset = sorted_list.pop(0)
            print(f"key:{row} offset:{offset} words found {count_dict[(row, offset)]}")
        if response == "y" or response == "Y":
            keep_going = False


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


def brute_force_rf(cipher: str, wordlist: []):
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
            candidate = decode_rf(cipher, key, offset)
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


def encode(plaintext: str, key: int, offset: int):
    period = 2 * key - 2
    rows = [[] for _ in range(key)]
    for i, char in enumerate(plaintext):
        row_index = key - 1 - abs(period // 2 - (i + offset) % period)
        rows[row_index] += plaintext[i]
    return ''.join(str(item) for inner_list in rows for item in inner_list)


if __name__ == "__main__":
    main()
