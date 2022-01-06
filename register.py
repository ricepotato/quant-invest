import logging
from reader import stock_csv_reader
from repository import MongodbRepository

log = logging.getLogger(__name__)


def resister_stocks(market: str, csv_filepath: str):
    repo = MongodbRepository()

    result = stock_csv_reader(csv_filepath)
    result_without_header = result[1:]
    kosdaq_stocks = repo.get_all(market)
    kosdaq_stock_dict = {}
    for stock in kosdaq_stocks:
        kosdaq_stock_dict[stock.code] = stock

    for stock in result_without_header:
        if stock.code not in kosdaq_stock_dict:
            log.info("add stock %s", stock)
            repo.add(stock)
