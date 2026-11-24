import random
from dataclasses import dataclass


@dataclass
class Session:
    name: str
    requests_left: int = 5

    @property
    def usable(self):
        return self.requests_left > 0

    def use(self):
        if not self.usable:
            raise RuntimeError(f'{self.name} exhausted')
        self.requests_left -= 1


class SessionRotator:
    def __init__(self, sessions):
        self.sessions = sessions
        self.current = 0

    def current_session(self):
        return self.sessions[self.current]

    def rotate_if_needed(self):
        if self.current_session().usable:
            return False
        for i, session in enumerate(self.sessions):
            if session.usable:
                self.current = i
                return True
        raise RuntimeError('All sessions exhausted')

    def run(self, task):
        self.rotate_if_needed()
        session = self.current_session()
        session.use()
        return f'{task} -> handled by {session.name} ({session.requests_left} left)'


def main():
    sessions = [
        Session(f'claude-session-{i + 1}', requests_left=random.randint(1, 3))
        for i in range(4)
    ]
    rotator = SessionRotator(sessions)
    for i in range(1, 11):
        try:
            print(rotator.run(f'task-{i}'))
        except RuntimeError as exc:
            print(exc)
            break


if __name__ == '__main__':
    main()