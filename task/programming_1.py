import csv
import os
from typing import Any, Dict


def _decoder(mapping: Dict[str, Any], message: str, word_separator: str, letter_separator: str):
    words = message.split(word_separator)
    r = []
    for word in words:
        letters = word.split(letter_separator)
        for letter in letters:
            if letter not in mapping:
                raise ValueError("Message cannot be decoded!")
            r.append(mapping[letter])
        r.append(' ')
    return ''.join(r)


class MorseDecoder:
    def __init__(self):
        data_directory = ".\\data"
        code_file = "morse.csv"

        # Read code data
        with open(os.path.join(data_directory, code_file)) as f:
            data = csv.reader(f)
            self.code_map = {code: letter for letter, code in data}

    def decode(self, message: str):
        return _decoder(mapping=self.code_map, message=message, word_separator="   ", letter_separator=" ")


decoder = MorseDecoder().decode

if __name__ == "__main__":
    print(decoder('.- -   -.. .- .-- -.   .-.. --- --- -.-   - ---   - .... .   . .- ... -'))
