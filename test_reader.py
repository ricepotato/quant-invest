from reader import stock_csv_reader


def test_reader_make_stock_list():
    result = stock_csv_reader("./data/KOSDAQ_2022.csv")
    result_without_header = result[1:]
    assert result_without_header

    result = stock_csv_reader("./data/KOSPI_2022.csv")
    result_without_header = result[1:]
    assert result_without_header
