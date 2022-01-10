from frp import CompanyGuideFinancialReportProvider


def test_company_guide_frp_mock():
    frp = CompanyGuideFinancialReportProvider()

    def get_test_html(*args, **kwargs):
        with open("053800_2022.html", "r") as f:
            return f.read()

    frp._get_html = get_test_html
    result = frp.get_financial_report("053800")
    assert result[0].period == "2016-12"
    assert result[0].roa == 7.14
    assert result[2].period == "2018-12"
    assert result[2].per == 20.34


def test_company_guide_frp():
    frp = CompanyGuideFinancialReportProvider()
    result = frp.get_financial_report("053800")
    assert result[0].period == "2016-12"
    assert result[0].roa == 7.14
    assert result[2].period == "2018-12"
    assert result[2].per == 20.34
