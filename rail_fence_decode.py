import click


@click.command()
@click.option('-t', '--plain-text', required=True, help='The plain text enclosed in quotes.')
@click.option('-k', '--key', required=True, type=int, help='The number of rows to use')
@click.option('-o', '--offset', required=True, type=int, help='Offset, repeats after 2(key-1)')
def main(plain_text, key, offset):
    print(decode(plain_text, key, offset))


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


if __name__ == "__main__":
    main()
