import random
import re
import string


def generate_password(pattern=r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+]).{12,}'):
    """Generate a random password that matches the given regex pattern."""
    allowed = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        password = ''.join(random.choice(allowed) for _ in range(12))
        if re.fullmatch(pattern, password):
            return password


def main():
    regex = r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+]).{12,}'
    password = generate_password(regex)
    print(password)


if __name__ == '__main__':
    main()
