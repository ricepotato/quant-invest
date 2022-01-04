from reader import reader


def test_reader_make_stock_list():
    result = reader("./data/KOSDAQ_2022.csv")
    result_without_header = result[1:]
    assert result_without_header
