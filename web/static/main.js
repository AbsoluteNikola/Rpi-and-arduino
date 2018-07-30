console.log('load main.js');
window.pressureChart = new function buildPressure(){
	var ctx = document.getElementById('pressureChart');
	console.log(ctx);
	var chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: [],
			datasets: [{
				label: "data",
				data: []
			}]
		},
	});
	return chart;
}

window.temperatureChart = new function buildTemperature(){
	var ctx = document.getElementById('temperatureChart');
	console.log(ctx);
	var chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: [],
			datasets: [
			{
				label: "№1",
				data: []
			},
			{
				label: "№2",
				data: []
			}
			]
		}
	});
	return chart;
}

function addData(data){
	for(var sensor in data){
		var chart = window[sensor + 'Chart'];
		
		if(!(data[sensor] instanceof Array))
			data[sensor] = [data[sensor]]
		var d = new Date();
		
		chart.data.labels.push(`${d.getMinutes()}:${d.getSeconds()}`);
		
		//delete first point if size > 60
		if(chart.data.labels.length > 60){
			chart.data.labels.shift();
			for (var i = 0; i < chart.data.datasets.length; i++) {
				chart.data.datasets[i].data.shift();
			}
		}
		// add new points
		for(var i = 0; i < data[sensor].length; i++){
			chart.data.datasets[i].data.push(data[sensor][i]);
		}
		chart.update();

	}
}

function getInfo(){
	$.ajax({
	    url:'getInfo'
	})
	  .done(addData)
}

setInterval(getInfo, 1000);