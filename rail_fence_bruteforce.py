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
    common_word_file = load_word_list("common_words_min_3_letters.txt")
    row, offset = brute_force(cipher_text, common_word_file)

    print(f"Row count is most likely {green}{row}{reset} with offset {green}{offset}{reset}")
    print("Decoding with most likely settings . . .")
    print()
    print(decode(cipher_text, row, offset))
    print()


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
                if word in candidate:
                    word_count += 1
            if word_count > highest_word_count:
                highest_word_count = word_count
                row_candidate = key
                offset_candidate = offset
    return row_candidate, offset_candidate


def load_word_list(path: str) -> []:
    with open(path, "r") as common_words:
        common_word_list = []
        while line := common_words.readline():
            common_word_list.append(line.strip())
        return common_word_list


if __name__ == "__main__":
    main()
