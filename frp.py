from typing import List
from abc import abstractmethod
import requests
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
        fr_list = map(lambda fr: fr.update({"code": code}), result)
        return [FinancialReport.from_dict(fr) for fr in fr_list]

    def _get_url(self, code: str) -> str:
        # https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN=
        return f"https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN="

    def _get_html(self, url) -> str:
        r = requests.get(url)
        r.raise_for_status()
        return r.text

    def _parse_html(self, html: str) -> List:
        return []
