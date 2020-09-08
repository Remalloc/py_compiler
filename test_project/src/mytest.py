from random import random


class Test(object):
    def __init__(self):
        self.a = int(random() * 1000)
        self.b = int(random() * 1000)
        print(f"a = {self.a}, b = {self.b}")

    def test_add(self):
        print(f"a + b = {self.a + self.b}")

    def test_sub(self):
        print(f"a - b = {self.a - self.b}")

    def test_mul(self):
        print(f"a * b = {self.a * self.b}")

    def test_div(self):
        print(f"a / b = {self.a / self.b}")
        print(f"a // b = {self.a // self.b}")

    def start(self):
        self.test_add()
        self.test_mul()
        self.test_div()
