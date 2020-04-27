# unittestplus

Bringing some things I like from pytest into unittest

## parametrize

Parametrize is a decorator version of [subtest](https://docs.python.org/3/library/unittest.html#unittest.TestCase.subTest)
from the stdlib. 

```python
import unittest
from unittestplus import parametrize

class TestDog(unittest.TestCase):
    @parametrize([
        {'name': 'Bruce'},
        {'name': 'Penelope'},
    ])
    def test_dog_name_only_params(self, name):
        dog = Dog(name=name)
        self.assertEqual(dog.name, name)
```

## function tests

This decorator allows a function test case that will be discovered by `python -m unittest discover`. There is
a [FunctionTestCase](https://docs.python.org/3/library/unittest.html?highlight=functiontestcase#unittest.FunctionTestCase)
in the stdlib but it looks like it's [ignored by the discoverer](https://bugs.python.org/issue22680)

```python
from unittestplus import testcase

@testcase
def test_sup_2(test):
    dog = Dog(name='Bruce', age=8)
    test.assertEqual(dog.age, 8)

```

## fixtures 

Fixtures are implemented as class descriptors borrowing a bit from pytest concepts . There is support for both function 
(setUp) and class (setUpClass) scope. 

```python
from unittestplus import fixture, TestCasePlus

@fixture()
def penelope_fixture():
    return Dog(name='Penelope', age=10)

class TestFixtureDecorator(TestCasePlus):
    penelope = penelope_fixture()

    def test_penelope_fixture(self):
        self.assertEqual(self.penelope.name, penelope_fixture()().name)
```

## Run the test suite

```bash
python3 -m unittest discover
```