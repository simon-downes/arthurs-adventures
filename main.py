import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} [{levelname}] - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from engine import Engine

def main():

    logging.info("Starting game")

    engine = Engine()

    try:
        engine.run()

    except SystemExit:
        pass

if __name__ == "__main__":
    main()
