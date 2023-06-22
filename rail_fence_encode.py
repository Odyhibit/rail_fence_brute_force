import click


@click.command()
@click.option('-t', '--plain-text', help='The plain text enclosed in quotes.')
@click.option('-k', '--key', help='The number of rows to use')
def main(plain_text, key):
    print(encode(plain_text, key))


def encode(plaintext: str, key: int, offset: int):
    period = 2 * key - 2
    rows = [[] for _ in range(key)]
    for i, char in enumerate(plaintext):
        row_index = key - 1 - abs(period // 2 - (i + offset) % period)
        rows[row_index] += plaintext[i]
    return ''.join(str(item) for inner_list in rows for item in inner_list)


if __name__ == "__main__":
    main()
