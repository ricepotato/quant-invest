$(document).ready(function() {
	get_result();

	$("#btn_add_er").click(function(e){
		var er = {};
		er.comp_code = $("#txt_comp").val();
		er.period = $("#txt_period").val();
		er.hold = $("#opt_hold").val();
		var year = $("#st_period_yaer").val();
		var month = $("#st_period_mon").val();
		er.st_date = year + "-" + month;

		add_er(er);
	});
});

function get_result(){
	$.ajax({
		"url":"/calc/list",
		"type":"GET",
		"dataType": "html"
	}).done(function(html){
		$("#calc-list-container").html(html);
	});
}

function add_er(er){
	$.ajax({
		"url":"/api/calc",
		"type":"POST",
		"data":er,
		"dataType": "json"
	}).done(function(json){
		location.reload();
	});
}

function er_delete(id){
	console.log("id=" + id)
	$.ajax({
		"url":"/calc/delete/" + id,
		"type":"GET",
	}).done(function(json){
		location.reload();
	});
}