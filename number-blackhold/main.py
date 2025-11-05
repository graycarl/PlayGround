def main(length: int) -> None:
    for start in range(1000, 2000):
        result = chain(start, length)
        print(f"Start: {start}, Length: {len(result)}, Chain: {' -> '.join(map(str, result))}")


def chain(start: int, length: int) -> list[int]:
    seen = [start]
    while True:
        next = next_numer(seen[-1], length)
        if next in seen:
            break
        seen.append(next)
    return seen


def next_numer(n: int, length: int) -> int:
    fmt = "{0:0" + str(length) + "d}"
    n_str = fmt.format(n)
    biggest = int("".join(sorted(n_str, reverse=True)))
    smallest = int("".join(sorted(n_str)))
    return biggest - smallest


if __name__ == "__main__":
    main(4)
