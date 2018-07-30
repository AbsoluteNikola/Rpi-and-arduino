console.log('ok_');
function buildItAll() {
	window.pressureChart = buildPressure();
	window.temperatureChart = buildTemperature();
}

function buildPressure(){
	ctx = document.getElementById('pressureChart');
	console.log(ctx);
	chart = new Chart(ctx, {
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

function buildTemperature(){
	ctx = document.getElementById('temperatureChart');
	console.log(ctx);
	chart = new Chart(ctx, {
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
		},
	});
	return chart;
}

function getinfo(){
	$.ajax({
	    url:'getInfo'
	})
	  .done(function(ans){
	  	alert(ans);
	  })
}