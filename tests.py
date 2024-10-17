from gc import collect

from flask import session

from main import BooksCollector
import pytest

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    # def test_add_new_book_add_two_books(self):
    #     # создаем экземпляр (объект) класса BooksCollector
    #     collector = BooksCollector()
    #
    #     # добавляем две книги
    #     collector.add_new_book('Гордость и предубеждение и зомби')
    #     collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    #
    #     # проверяем, что добавилось именно две
    #     # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
    #     assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.fixture(scope="session")
    def set_up_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Человек паук')
        collector.set_book_genre('Человек паук', 'Фантастика')
        collector.add_new_book('Пила')
        collector.set_book_genre('Пила', 'Ужасы')
        collector.add_new_book('Шерлок Хоумс')
        collector.set_book_genre('Шерлок Хоумс', 'Детектив')
        return collector

    # Проверяем добавение нескольких книг
    def test_add_book_add_tree_books(self):
        collector = BooksCollector()
        collector.add_new_book('Hobbit')
        collector.add_new_book('Harry Potter')
        collector.add_new_book('Мертвые души')

        assert len(collector.get_books_genre()) == 3, (
            f'Ожидаемый результат 3, фактический результат {len(collector.get_books_genre())}'
        )

    # Проверка добавления книги с названием > 40 символов или пустым значением
    @pytest.mark.parametrize('book', ['', '12345678901234567890123456789012345678901'])
    def test_add_book_invalid_format(self, book):
        collector = BooksCollector()
        collector.add_new_book(book)
        assert len(collector.get_books_genre()) == 0, (
                    f'Ожидаемый результат 0, фактический результат {len(collector.get_books_genre())}')

    # Проверка установки книге жанра который есть в списке
    def test_set_book_genre_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Чип и Дейл")
        collector.set_book_genre('Чип и Дейл', 'Мультфильмы')
        assert collector.get_books_genre() == {"Чип и Дейл": "Мультфильмы"}

    # Проверка установки книге жанра которого нет в списке
    def test_set_book_genre_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Alladin')
        collector.set_book_genre('Alladin', 'Документальный')
        assert collector.get_books_genre() == {'Alladin': ''}


    @pytest.mark.parametrize('genre , book', [('Фантастика', ["Человек паук"]),
                                              ('Ужасы', ["Пила"]),
                                              ('Комедии', [])])
    # Проверка вывода списка книг с определённым жанром
    def test_get_books_with_specific_genre(self, set_up_books_genre, genre, book):
        assert set_up_books_genre.get_books_with_specific_genre(genre) == book

    # Проверка вывода списка книг для детей
    def test_get_books_for_children(self, set_up_books_genre):
        print(set_up_books_genre.get_books_for_children())
        assert set_up_books_genre.get_books_for_children() == ['Человек паук']

    # Проверка вывода книги с неподходящим жанром для детей
    def test_get_books_for_children_horror(self, set_up_books_genre):
        set_up_books_genre.books_genre['Человек паук'] = ""
        print(set_up_books_genre.books_genre)
        assert set_up_books_genre.get_books_for_children() == []