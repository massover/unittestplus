import unittest
from dataclasses import dataclass

from unittestplus import parametrize, testcase, TestCasePlus, Fixture, fixture


@dataclass
class Dog:
    name: str
    age: int = 0


class CharlieFixture(Fixture):
    def __call__(self):
        return Dog(name='Charlie', age=1)


class CharlieClassFixture(Fixture):
    scope = 'class'

    def __call__(self):
        return Dog(name='Charlie', age=1)


def bruce_fixture():
    return Dog(name='Bruce', age=8)


@fixture()
def penelope_fixture():
    return Dog(name='Penelope', age=10)


@fixture(scope='class')
def penelope_class_fixture():
    return Dog(name='Penelope', age=10)


class TestDog(unittest.TestCase):
    @parametrize([
        ('Name is Bruce', {'name': 'Bruce'}),
        ('Name is Peneloope', {'name': 'Penelope'}),
    ])
    def test_dog_name_msg_and_params(self, name):
        dog = Dog(name=name)
        self.assertEqual(dog.name, name)

    @parametrize([
        {'name': 'Bruce'},
        {'name': 'Penelope'},
    ])
    def test_dog_name_only_params(self, name):
        dog = Dog(name=name)
        self.assertEqual(dog.name, name)


class TestFixtureClass(TestCasePlus):
    bruce = Fixture(fn=bruce_fixture)
    bruce_class = Fixture(fn=bruce_fixture, scope='class')
    charlie = CharlieFixture()
    charlie_class = CharlieClassFixture()

    def test_bruce_func_fixture(self):
        self.assertEqual(self.bruce.name, bruce_fixture().name)
        self.bruce.name = 'lol'

    def test_bruce_func_fixture_is_recreated(self):
        self.assertEqual(self.bruce.name, bruce_fixture().name)

    def test_bruce_class_fixture(self):
        self.assertEqual(self.bruce_class.name, bruce_fixture().name)
        self.bruce_class.name = 'lol'

    def test_bruce_class_fixture_was_modified(self):
        self.assertEqual(self.bruce_class.name, 'lol')

    def test_charlie_func_fixture(self):
        self.assertEqual(self.charlie.name, CharlieFixture()().name)
        self.charlie.name = 'lol'

    def test_charlie_func_fixture_is_recreated(self):
        self.assertEqual(self.charlie.name, CharlieFixture()().name)

    def test_charlie_class_fixture(self):
        self.assertEqual(self.charlie_class.name, CharlieFixture()().name)
        self.charlie_class.name = 'lol'

    def test_charlie_class_fixture_was_modified(self):
        self.assertEqual(self.charlie_class.name, 'lol')


class TestFixtureDecorator(TestCasePlus):
    penelope = penelope_fixture()
    penelope_class = penelope_class_fixture()
    penelope_class_to_func = penelope_class_fixture(scope='func')

    def test_penelope_fixture(self):
        self.assertEqual(self.penelope.name, penelope_fixture()().name)
        self.penelope.name = 'lol'

    def test_penelope_fixture_is_recreated(self):
        self.assertEqual(self.penelope.name, penelope_fixture()().name)

    def test_penelope_class(self):
        self.assertEqual(self.penelope_class.name, penelope_class_fixture()().name)
        self.penelope_class.name = 'lol'

    def test_penelope_class_was_modified(self):
        self.assertEqual(self.penelope_class.name, 'lol')

    def test_penelope_class_to_func(self):
        self.assertEqual(self.penelope_class_to_func.name, penelope_class_fixture()().name)
        self.penelope_class_to_func.name = 'lol'

    def test_penelope_class_to_func_is_recreated(self):
        self.assertEqual(self.penelope_class_to_func.name, penelope_class_fixture()().name)


@testcase
def test_dog_age(test):
    dog = Dog(name='Bruce', age=8)
    test.assertEqual(dog.age, 8)

