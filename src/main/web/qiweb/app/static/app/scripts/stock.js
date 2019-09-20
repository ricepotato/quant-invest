
$(document).ready(function() {
	$('#stock_tbl').DataTable( {
		"processing": true,
        "serverSide": true,
        "ajax": "/api/stock?market=KOSPI&year=2018"
	});
});