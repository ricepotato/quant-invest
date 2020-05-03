from bs4 import BeautifulSoup
import requests

def get_stock_info(gicode, row_name):
    try:
        url = 'http://comp.fnguide.com/SVO2/asp/SVD_Main.asp?pGB=1&gicode=A' + gicode
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('div', {'id': 'svdMainGrid10D'})

        per_text = table.find(text=row_name)
        per = per_text.find_next(class_='r').text

        return per

    except Exception as e:
        print(e)

def print_stack_info(gicode):
    print(get_stock_info(gicode, 'PER'))
    print(get_stock_info(gicode, 'ROE'))

print_stack_info('005930')
