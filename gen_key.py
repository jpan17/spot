from os import urandom

# Good for generating secret key (for .env)

if __name__ == '__main__':
    print(urandom(24))