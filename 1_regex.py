from typing import Generator


def prime(func):
    def wrapper(*args, **kwargs):
        v = func(*args, **kwargs)
        next(v)
        return v

    return wrapper


class RegexFSM:
    def __init__(self):
        self.start = self._create_start()
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()

        self.current_state: Generator = self.start
        self.stopped = False

    def send(self, char):
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    def does_match(self):
        if self.stopped:
            return False
        return self.current_state is self.q3

    @prime
    def _create_start(self):
        while True:
            char = yield
            if char == 'a':
                self.current_state = self.q1
            else:
                break

    @prime
    def _create_q1(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q2
            elif char == 'c':
                self.current_state = self.q3
            else:
                break

    @prime
    def _create_q2(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q2
            elif char == 'c':
                self.current_state = self.q3
            else:
                break

    @prime
    def _create_q3(self):
        while True:
            char = yield
            break


def grep_text(text):
    evaluator = RegexFSM()
    for ch in text:
        evaluator.send(ch)
    return evaluator.does_match()


if __name__ == '__main__':
    "ab*c"
    assert not grep_text('a')
    assert not grep_text('ab')
    assert grep_text('abc')
    assert grep_text('abbbbbbc')
    assert not grep_text('abbbbbbccccc')
    assert grep_text('ac')
    assert not grep_text('acccc')
