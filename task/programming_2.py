def encode(message: str) -> str:
    return ' '.join([s[::-1] if len(s) > 3 else s for s in message.split(' ')])


if __name__ == "__main__":
    print(encode("AT DAWN LOOK TO THE EAST"))
