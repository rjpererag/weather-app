import os


def setup_environment():
    if not os.path.exists("logs"):
        os.makedirs("logs")


def main():
    setup_environment()


if __name__ == "__main__":
    main()

