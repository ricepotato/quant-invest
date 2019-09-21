
var year = "2018"
var market = "KOSPI"
var dt = null;

$(document).ready(function() {
	dt = create_table();
	btn_add_event();
});

function create_table(){
	dt = $('#stock_tbl').DataTable( {
		"processing": true,
		"serverSide": true,
		"searching": false,
		"ajax": {
            "url": "/api/stock",
            "data": function ( d ) {
				d.market = market;
				d.year = year;
                // d.custom = $('#myInput').val();
                // etc
            }
        }
	});

	return dt;
}

function btn_add_event(){
	$("#btn_refresh").click(function(){
		dt.ajax.reload();
	});
	$("#btn_year_2018").click(function(){
		year = "2018";
		$("#cur_year").text(year);
		dt.ajax.reload();
	});
	$("#btn_year_2017").click(function(){
		year = "2017";
		$("#cur_year").text(year);
		dt.ajax.reload();
	});
	$("#btn_year_2016").click(function(){
		year = "2016";
		$("#cur_year").text(year);
		dt.ajax.reload();
	});

	$("#btn_mrk_kospi").click(function(){
		market = "KOSPI";
		$("#cur_mrk").text(market);
		dt.ajax.reload();
	});

	$("#btn_mrk_kosdaq").click(function(){
		market = "KOSDAQ";
		$("#cur_mrk").text(market);
		dt.ajax.reload();
	});
}