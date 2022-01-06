import sys
import logging
import dotenv
from register import resister_stocks

dotenv.load_dotenv()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def main():
    resister_stocks("KOSDAQ", "./data/KOSDAQ_2022.csv")
    resister_stocks("KOSPI", "./data/KOSPI_2022.csv")


if __name__ == "__main__":
    sys.exit(main())
