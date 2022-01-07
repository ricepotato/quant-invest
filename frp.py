from typing import List
from abc import abstractmethod
import requests
from bs4 import BeautifulSoup as BS
from models import FinancialReport


class FinancialReportProvider:
    @abstractmethod
    def get_financial_report(self, code: str) -> List[FinancialReport]:
        pass


class CompanyGuideFinancialReportProvider(FinancialReportProvider):
    def get_financial_report(self, code: str) -> List[FinancialReport]:
        url = self._get_url()
        html = self._get_html(url)
        result = self._parse_html(html)

        def _ufr(fr):
            fr["code"] = code
            return fr

        fr_list = map(_ufr, result)
        return [FinancialReport.from_dict(fr) for fr in fr_list]

    def _get_url(self, code: str) -> str:
        # https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN=
        return f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN="

    def _get_html(self, url) -> str:
        r = requests.get(url)
        r.raise_for_status()
        return r.text

    def _parse_html(self, html: str) -> List:
        bs = BS(html, "html.parser")
        result = []
        # res = {}
        # res["period"] = {}
        sel_mrk = "#svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)"
        # svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)
        # svdMainGrid1 > table > tbody > tr:nth-child(5) > td:nth-child(2)
        market_cap = self._get_text_from_selector(bs, sel_mrk)
        # res["market_cap"] = int(market_cap)
        for idx in range(1, 6):
            sel_period = f"#highlight_D_Y > table > thead > tr.td_gapcolor2 > th:nth-child({idx})"
            sel_roa = f"#highlight_D_Y > table > tbody > tr:nth-child(16) > td:nth-child({idx+1})"
            sel_roe = f"#highlight_D_Y > table > tbody > tr:nth-child(17) > td:nth-child({idx+1})"
            sel_per = f"#highlight_D_Y > table > tbody > tr:nth-child(21) > td:nth-child({idx+1})"
            sel_pbr = f"#highlight_D_Y > table > tbody > tr:nth-child(22) > td:nth-child({idx+1})"

            period = self._get_text_from_selector(bs, sel_period)
            roa = self._str_to_float(self._get_text_from_selector(bs, sel_roa))
            roe = self._str_to_float(self._get_text_from_selector(bs, sel_roe))
            per = self._str_to_float(self._get_text_from_selector(bs, sel_per))
            pbr = self._str_to_float(self._get_text_from_selector(bs, sel_pbr))
            period = period.replace("/", "-")
            # res["period"][period] = {"roa": roa, "roe": roe, "per": per, "pbr": pbr}

            result.append(
                {
                    "period": period,
                    "roa": roa,
                    "roe": roe,
                    "per": per,
                    "pbr": pbr,
                    "market_cap": int(market_cap),
                }
            )

        return result

    def _get_text_from_selector(self, bs, selector):
        obj = bs.select(selector)
        return obj[0].text.strip().replace(",", "")
