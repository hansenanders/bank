
function drawChart(data, categorys) {
    headers = data.shift(); // Headers
    headers = ['Date', 'Transaction', 'Balance']
    chart_data = [headers];
    for (d in data) {
	var transaction = parseFloat(data[d][3]);
	if (!Number.isInteger(transaction)) {
	    transaction = transaction * 1000;
	}

	var balance = parseFloat(data[d][4]);
	if (!Number.isInteger(balance)) {
	    balance = balance * 1000;
	}

	chart_data.push([new Date(data[d][0]), transaction, balance]);
    }
//    console.log(arrayData);

    var data = google.visualization.arrayToDataTable(chart_data);
    var options = {
        title: 'Company Performance',
        curveType: 'function',
        legend: { position: 'bottom' },
	explorer: { actions: ['dragToZoom', 'rightClickToReset']}
    };
    
    var chart = new google.visualization.LineChart(document.getElementById('chart'));
    
    chart.draw(data, options);
}

$(document).ready(function() {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(start);
    function start() {
	get_csv_data();
    }

    function get_categorys() {
	$.ajax({
	    dataType: "json",
	    url: '/data/categorys',
	    type: 'POST',
	    success: function(response) {
		categorys = response;
		console.log(response);
		drawChart(csv_data, categorys);
	    },
	    error: function(error) {
		console.log(error);
	    }
	});
    }
    
    function get_csv_data() {
	$.ajax({
	    url: '/data',
	    type: 'POST',
	    success: function(response) {
		csv_data = $.csv.toArrays(response, {onParseValue: $.csv.hooks.castToScalar});
		get_categorys();
	    },
	    error: function(error) {
		console.log(error);
	    }});
    }
});
