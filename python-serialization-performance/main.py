"""
Test the performance of many serialization tools.
"""
import datetime
import random
import dataclasses
import timeit
import msgspec


class Book:
    title: str
    isbn: str
    published: datetime.date
    pages: int
    description: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Author:
    name: str
    age: int
    description: str
    gender: str
    email: str
    phone: str
    birthday: datetime.date
    books: list[Book]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Group:
    authors: list[Author]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@dataclasses.dataclass
class BookDC:
    title: str
    isbn: str
    published: datetime.date
    pages: int
    description: str


@dataclasses.dataclass
class AuthorDC:
    name: str
    age: int
    description: str
    gender: str
    email: str
    phone: str
    birthday: datetime.date
    books: list[BookDC]


@dataclasses.dataclass
class GroupDC:
    authors: list[AuthorDC]


class BookMP(msgspec.Struct):
    title: str
    isbn: str
    published: datetime.date
    pages: int
    description: str


class AuthorMP(msgspec.Struct):
    name: str
    age: int
    description: str
    gender: str
    email: str
    phone: str
    birthday: datetime.date
    books: list[BookMP]


class GroupMP(msgspec.Struct):
    authors: list[AuthorMP]


class BookMPNoGC(msgspec.Struct, gc=False):
    title: str
    isbn: str
    published: datetime.date
    pages: int
    description: str


class AuthorMPNoGC(msgspec.Struct, gc=False):
    name: str
    age: int
    description: str
    gender: str
    email: str
    phone: str
    birthday: datetime.date
    books: list[BookMPNoGC]


class GroupMPNoGC(msgspec.Struct, gc=False):
    authors: list[AuthorMPNoGC]


def _random_book() -> dict:
    return {
        "title": "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        "isbn": "".join(random.choices("0123456789", k=13)),
        "published": datetime.date.today(),
        "pages": random.randint(100, 1000),
        "description": "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=200)),
    }


def _random_author() -> dict:
    return {
        "name": "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        "age": random.randint(20, 80),
        "description": "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=200)),
        "gender": random.choice('MF'),
        "email": "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)) + "@example.com",
        "phone": "".join(random.choices("0123456789", k=10)),
        "birthday": datetime.date.today(),
    }


def random_group_plain(authors=50, books=50) -> Group:
    return Group(authors=[
        Author(**_random_author(), books=[Book(**_random_book())
                                          for _ in range(books)])
        for _ in range(authors)
    ])


def random_group_dc(authors=50, books=50) -> GroupDC:
    return GroupDC(authors=[
        AuthorDC(**_random_author(), books=[BookDC(**_random_book())
                                            for _ in range(books)])
        for _ in range(authors)
    ])


def random_group_mp(authors=50, books=50) -> GroupMP:
    return GroupMP(authors=[
        AuthorMP(**_random_author(), books=[BookMP(**_random_book())
                                            for _ in range(books)])
        for _ in range(authors)
    ])


def random_group_mp_nogc(authors=50, books=50) -> GroupMPNoGC:
    return GroupMPNoGC(authors=[
        AuthorMPNoGC(**_random_author(), books=[BookMPNoGC(**_random_book())
                                                for _ in range(books)])
        for _ in range(authors)
    ])


def main():
    import pickle
    import sys

    print("Testing environment:")
    print("  Python:", sys.version)
    print("  Msgspec:", msgspec.__version__)

    group = random_group_plain()
    group_dc = random_group_dc()
    group_mp = random_group_mp()
    group_mp_nogc = random_group_mp_nogc()

    print("Pickle + Plain:")
    data = pickle.dumps(group)
    print("  Size:", len(data))
    print("  Serialize:", timeit.timeit(lambda: pickle.dumps(group), number=100))
    print("  Deserialize:", timeit.timeit(lambda: pickle.loads(data), number=100))

    print("Pickle + Dataclass:")
    data = pickle.dumps(group_dc)
    print("  Size:", len(data))
    print("  Serialize:", timeit.timeit(lambda: pickle.dumps(group_dc), number=100))
    print("  Deserialize:", timeit.timeit(lambda: pickle.loads(data), number=100))

    for scheme in ['json', 'msgpack']:
        print(f"Msgspec[{scheme}] + Dataclass:")
        module = getattr(msgspec, scheme)
        data = module.encode(group_dc)
        # open('/tmp/data.json', 'wb').write(data)
        print("  Size:", len(data))
        print("  Serialize:", timeit.timeit(lambda: module.encode(group_dc), number=100))
        print("  Deserialize:", timeit.timeit(lambda: module.decode(data, type=GroupDC), number=100))

        print(f"Msgspec[{scheme}] + Struct:")
        data = module.encode(group_mp)
        print("  Size:", len(data))
        print("  Serialize:", timeit.timeit(lambda: module.encode(group_mp), number=100))
        print("  Deserialize:", timeit.timeit(lambda: module.decode(data, type=GroupMP), number=100))

        print(f"Msgspec[{scheme}] + Struct (no GC):")
        data = module.encode(group_mp_nogc)
        print("  Size:", len(data))
        print("  Serialize:", timeit.timeit(lambda: module.encode(group_mp_nogc), number=100))
        print("  Deserialize:", timeit.timeit(lambda: module.decode(data, type=GroupMPNoGC), number=100))


if __name__ == "__main__":
    main()
