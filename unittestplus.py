import unittest

import functools


def parametrize(iterable):
    def inner(method):
        @functools.wraps(method)
        def wrapped(instance, *args, **kwargs):
            for msg_params in iterable:
                if isinstance(msg_params, dict):
                    msg = ''
                    params = msg_params
                else:
                    msg = msg_params[0]
                    params = msg_params[1]
                with instance.subTest(msg=msg, **params):
                    return method(instance, *args, **params, **kwargs)
        return wrapped
    return inner


def testcase(func):
    func_name = func.__name__
    if func_name.startswith('test') or func_name.endswith('test'):
        test_func_name = func_name
    else:
        test_func_name = f"test_{func.__name__}"
    testcase_name = f"TestCase__{func.__name__}"

    def method(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return type(testcase_name, (unittest.TestCase, ), {
        func_name: method
    })


class Fixture:
    FUNC_SCOPE = 'func'
    CLASS_SCOPE = 'class'
    scope = None

    def __init__(self, fn=None, scope=None):
        scope = scope or self.scope or self.FUNC_SCOPE
        super().__init__()
        assert scope in [self.CLASS_SCOPE, self.FUNC_SCOPE], \
            f"Invalid scope choice: {scope}. "
        self.fn = fn
        self.scope = scope
        self._fixture = None

    def __call__(self):
        return self.fn()

    def __get__(self, instance, owner):
        if self.name in instance._class_fixtures_cache:
            self._fixture = instance._class_fixtures_cache[self.name]
        elif self._fixture is None:
            self._fixture = self()
        return self._fixture

    def __set__(self, instance, value):
        self._fixture = value

    def __set_name__(self, owner, name):
        self.name = name


def func_filter(fixtures):
    return [(k, v) for k, v in fixtures.items() if v.scope == v.FUNC_SCOPE]


def class_filter(fixtures):
    return [(k, v) for k, v in fixtures.items() if v.scope == v.CLASS_SCOPE]


class TestCasePlus(unittest.TestCase):
    _class_fixtures_cache = {}
    _fixtures = {}

    @classmethod
    def setUpClass(cls):
        super(TestCasePlus, cls).setUpClass()
        for name, value in cls.__dict__.items():
            if not isinstance(value, Fixture):
                continue
            cls._fixtures[name] = value

        for name, fixture in class_filter(cls._fixtures):
            cls._class_fixtures_cache[name] = fixture()

    def tearDown(self) -> None:
        for name, fixture in func_filter(self._fixtures):
            setattr(self, name, None)

    @classmethod
    def tearDownClass(cls) -> None:
        for name, fixture in class_filter(cls._fixtures):
            setattr(cls, name, None)

        cls._class_fixtures_cache = {}


def fixture(scope=Fixture.FUNC_SCOPE):
    default_scope = scope

    def inner(func):
        @functools.wraps(func)
        def wrapped(scope=None):
            scope = scope or default_scope
            return Fixture(func, scope=scope)
        return wrapped

    return inner
