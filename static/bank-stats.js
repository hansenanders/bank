function draw_line_chart(data) {
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

    var chart = new google.visualization.LineChart(document.getElementById('linechart'));

    chart.draw(data, options);
}

function draw_pie_chart(transactions, categories) {
    console.log(transactions);
    console.log(categories);

    var display_data = {};
    var values = Object.values(categories);
    for (var v in values) {
	display_data[values[v]] = 0;
    }


    var deposits = 0;
    var withdraws = 0;
    for (var t in transactions) {
	var value = transactions[t]['value'];
	if (value >= 0) {
	    deposits += value;
	} else {
	    withdraws += value;
	}

	var transaction_category = categories[t];
	display_data[transaction_category] += value;
    }
    console.log('deposits: ' + deposits);
    console.log('withdraws: ' + withdraws);
    console.log(display_data);

    // Define the chart to be drawn.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Browser');
    data.addColumn('number', 'Percentage');
    data.addRows([
	['Firefox', 45.0],
	['IE', 26.8],
	['Chrome', 12.8],
	['Safari', 8.5],
	['Opera', 6.2],
	['Others', 0.7]
    ]);

   // Set chart options
    var options = {'title':'Browser market shares at a specific website, 2014',
		   'width':550,
		   'height':400};

    // Instantiate and draw the chart.
    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);
}

$(document).ready(function() {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(start);
    function start() {
	get_transactions();
    }

    function get_categories(transactions) {
	$.ajax({
	    dataType: "json",
	    url: '/data/categories',
	    type: 'POST',
	    success: function(response) {
		draw_pie_chart(transactions, response);
//		draw_line_chart(csv_data);
	    },
	    error: function(error) {
		console.log(error);
	    }
	});
    }

    function get_transactions() {
	$.ajax({
	    dataType: "json",
	    url: '/data/transactions',
	    type: 'POST',
	    success: function(response) {
		get_categories(response);
	    },
	    error: function(error) {
		console.log(error);
	    }});
    }
});
