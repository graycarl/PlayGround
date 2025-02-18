class Book:

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

    def __str__(self):
        return f'{self.title} by {self.author}'

    def __repr__(self):
        return f'Book({self.isbn}, {self.title}, {self.author})'

    def __eq__(self, other):
        return self.isbn == other.isbn

    def __hash__(self):
        return hash(self.isbn)


class Book2:

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

    def __str__(self):
        return f'{self.title} by {self.author}'

    def __repr__(self):
        return f'Book2({self.isbn}, {self.title}, {self.author})'

    def __eq__(self, other):
        return (self.isbn, self.title, self.author) == (other.isbn, other.title, other.author)

    def __hash__(self):
        return hash(self.isbn)


def main():
    book1 = Book('978-3-16-148410-0', 'The Great Gatsby', 'F. Scott Fitzgerald')
    book2 = Book('978-3-16-148410-0', 'The Great Gatsby', 'F. Scott Fitzgerald xx')
    book3 = Book('978-3-16-148410-1', 'The Great Gatsby', 'F. Scott Fitzgerald')

    assert book1 == book2
    assert book1 != book3

    assert len(set([book1, book2, book3])) == 2

    book4 = Book2('978-3-16-148410-0', 'The Great Gatsby', 'F. Scott Fitzgerald')
    book5 = Book2('978-3-16-148410-0', 'The Great Gatsby', 'F. Scott Fitzgerald xx')
    book6 = Book2('978-3-16-148410-1', 'The Great Gatsby', 'F. Scott Fitzgerald')

    assert book4 != book5
    assert book4 != book6

    assert len(set([book4, book5, book6])) == 3


if __name__ == '__main__':
    main()
