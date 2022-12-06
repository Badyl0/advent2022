if __name__ == "__main__":
    with open("inputs.txt") as inputs:
        datagram = inputs.read()
    size = 14
    for index, value in enumerate(datagram):
        chunk = set(datagram[index:index + size])
        print(datagram[index:index + size])
        if len(chunk) == size:
            print(index+size)
            print(chunk)
            break
