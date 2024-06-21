import pytest
from main import BooksCollector


class TestBooksCollector:
    books_to_add = [
        ('Мгла', 'Ужасы'),
        ('Гарри Поттер', 'Фантастика'),
        ('Дюна', 'Фантастика'),
        ('Оно', 'Ужасы'),
        ('Призрак', 'Ужасы')
    ]

    @pytest.mark.parametrize('valid', ['А', 'А' * 40])
    def test_add_new_book_valid_name_true(self, valid):
        book = BooksCollector()
        book.add_new_book(valid)
        assert valid in book.books_genre

    @pytest.mark.parametrize('invalid', [''])
    def test_add_new_book_empty_name(self, invalid):
        book = BooksCollector()
        book.add_new_book(invalid)
        assert not invalid in book.books_genre

    @pytest.mark.parametrize('invalid', ['А' * 41])
    def test_add_new_book_too_long_name(self, invalid):
        book = BooksCollector()
        book.add_new_book(invalid)
        assert not invalid in book.books_genre

    def test_set_book_genre_true(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.set_book_genre('Мгла', 'Ужасы')
        assert book.get_book_genre('Мгла') == 'Ужасы'

    def test_set_book_genre_no_name(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.set_book_genre('Мгла', 'Научные')
        assert book.get_book_genre('Мгла') == ''

    def test_set_book_genre_no_book_true(self):
        book = BooksCollector()
        book.set_book_genre('Мгла', 'Ужасы')
        assert 'Мгла' not in book.books_genre

    def test_get_book_genre_if_genre_exist_true(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.set_book_genre('Мгла', 'Ужасы')
        assert book.get_book_genre('Мгла') == 'Ужасы'

    def test_get_book_genre_if_genre_not_set(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        assert book.get_book_genre('Мгла') == ''

    def test_get_book_genre_if_book_not_exist(self):
        book = BooksCollector()
        assert book.get_book_genre('Книга') is None

    def test_get_books_with_specific_genre_add_different_genres_true(self):
        book = BooksCollector()
        for film, genre in self.books_to_add:
            book.add_new_book(film)
            book.set_book_genre(film, genre)
        horror_books = book.get_books_with_specific_genre('Ужасы')
        assert 'Мгла' in horror_books
        assert 'Оно' in horror_books
        assert 'Призрак' in horror_books
        assert len(horror_books) == 3

    def test_get_books_with_specific_genre_without_books_true(self):
        book = BooksCollector()
        book.get_books_with_specific_genre('Ужасы')
        assert len(book.get_books_with_specific_genre('Ужасы')) == 0

    def test_get_books_with_specific_genre_no_books_of_genre(self):
        book = BooksCollector()
        for film, genre in self.books_to_add:
            book.add_new_book(film)
            book.set_book_genre(film, genre)
        detective_books = book.get_books_with_specific_genre('Детективы')
        assert len(detective_books) == 0

    def test_get_books_with_specific_genre_not_valid_genre(self):
        book = BooksCollector()
        for film, genre in self.books_to_add:
            book.add_new_book(film)
            book.set_book_genre(film, genre)
        empty_genre_books = book.get_books_with_specific_genre('Научные')
        assert len(empty_genre_books) == 0

    @pytest.mark.parametrize('books_to_add', [[('Мгла', 'Ужасы'), ('Гарри Поттер', 'Фантастика')]])
    def test_get_books_genre_few_genres_true(self, books_to_add):
        book = BooksCollector()
        for film, genre in books_to_add:
            book.add_new_book(film)
            book.set_book_genre(film, genre)
        assert len(book.get_books_genre()) == 2

    def test_get_books_genre_empty_books_list_true(self):
        book = BooksCollector()
        assert len(book.get_books_genre()) == 0

    @pytest.mark.parametrize('books_to_add', [[('Книга смеха', 'Комедии'), ('Гарри Поттер', 'Фантастика')]])
    def test_get_books_for_children_true(self, books_to_add):
        book = BooksCollector()
        for film, genre in books_to_add:
            book.add_new_book(film)
            book.set_book_genre(film, genre)
        assert len(book.get_books_for_children()) == 2

    @pytest.mark.parametrize('books_to_add', [[('Мгла', 'Ужасы'), ('Тайна', 'Детективы')]])
    def test_get_books_for_children_excludes_adult_genres(self, books_to_add):
        book = BooksCollector()
        for name, genre in books_to_add:
            book.add_new_book(name)
            book.set_book_genre(name, genre)
        assert len(book.get_books_for_children()) == 0

    def test_add_book_in_favorites_true(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.add_book_in_favorites('Мгла')
        assert 'Мгла' in book.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_false(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.add_book_in_favorites('Мгла')
        book.add_book_in_favorites('Мгла')
        assert book.get_list_of_favorites_books() == ['Мгла']

    def test_delete_book_from_favorites_true(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.add_book_in_favorites('Мгла')
        book.delete_book_from_favorites('Мгла')
        assert 'Мгла' not in book.get_list_of_favorites_books()

    def test_delete_book_from_favorites_false(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.delete_book_from_favorites('Мгла')
        assert 'Мгла' not in book.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_true(self):
        book = BooksCollector()
        book.add_new_book('Мгла')
        book.add_book_in_favorites('Мгла')
        assert book.get_list_of_favorites_books() == ['Мгла']
