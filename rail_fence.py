#!/usr/bin/env python
import click


@click.command()
@click.version_option(version="0.4", prog_name="rail_fence")
@click.option('-t', '--text', required=True, help='Text enclosed in quotes.')
@click.option('-k', '--key', type=int, help='The number of rows to use')
@click.option('-o', '--offset', default=0, show_default=True, type=int, help='Offset, repeats after 2(key-1)')
@click.option('--decode/--encode', '-d/-e', default=True, show_default=True)
@click.option('--brute-force', '-b', is_flag=True)
@click.option('--show-all', '-a', is_flag=True, help="Send all possible decryption to standard output")
def main(text, key, offset, decode, brute_force, show_all):
    cipher_text = text
    common_words_longest_first = load_word_list("common_words.txt")

    if cipher_text is None:
        print("Nothing to solve, please give me some cipher text.")
        return

    if show_all and not brute_force:
        print("show-all only works with brute force mode")
        return

    if not decode:
        print(f'Encoding With Key:{key} Offset:{offset}')
        print(encode(text, key, offset))
        print()
        return

    if decode and not brute_force:
        if key is None:
            print('Either a key or the brute-force flag are required to decode.')
            print()
            return
        else:
            print(f'Decoding With Key:{key} Offset:{offset}')
            print(decode_rf(text, key, offset))
            print()
            return

    if decode and brute_force:
        row, offset, count_dict = brute_force_rf(cipher_text, common_words_longest_first)
        print(f"Using key:{row} offset:{offset} words found use {count_dict[(row, offset)]} of the letters")
        print("Decoding with most likely settings . . .")
        print()

        sorted_list = sorted(count_dict, key=count_dict.get, reverse=True)
        if show_all:
            for (row, offset) in sorted_list:
                print(decode_rf(cipher_text, row, offset))
            return

        sorted_list.pop(0)
        keep_going = True
        while keep_going:
            print(decode_rf(cipher_text, row, offset))
            print()

            response = input(f"Does that look correct (y/n/a)\n yes, no, show all(most likely first)")
            if response in {"n", "N"}:
                row, offset = sorted_list.pop(0)
                print(f"key:{row} offset:{offset} words found use {count_dict[(row, offset)]} of the letters")
            if response in {"Y", "y"}:
                return
            if response in {"A", "a"} or show_all:
                for (row, offset) in sorted_list:
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
    """recursively removes the word and then looks again keeping a count
       Returns: count of how many times the word occurred, and the text with the word removed
    """
    index = haystack.find(needle)
    if index == -1:
        return current_count, haystack
    new_haystack = haystack[:index] + haystack[index + len(needle):]
    current_count += len(needle)
    return count_and_remove(needle, new_haystack, current_count)


def load_word_list(path: str) -> []:
    """Returns a list of words in the file with the longest first."""
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
