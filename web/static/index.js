console.log('load main.js');

window.temperatureChart = new function buildTemperature(){
	var ctx = document.getElementById('temperatureChart');
	var chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: [],
			datasets: [
			{
				label: "№1",
				data: [],
				borderColor: 'rgb(0, 105, 217)',
				fill: false
			},
			{
				label: "№2",
				data: [],
				borderColor: 'rgb(255, 169, 0)',
				fill: false
			}
			]
		},
		options: {
			title: {
				display: true,
				text: 'Temperature'
			}
		}
	});
	console.log('temperatureChart was built');
	return chart;
}

window.humidityChart = new function buildHumidity(){
	var ctx = document.getElementById('humidityChart');
	var chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: [],
			datasets: [
			{
				label: "",
				data: [],
				borderColor: 'rgb(0, 105, 217)',
				backgroundColor: 'rgba(0, 105, 217, 0.2)'
			}
			]
		},
		options: {
			title: {
				display: true,
				text: 'Humidity'
			}
		}
	});
	console.log('humidityChart was built');
	return chart;
}


window.CO2Chart = new function buildCO2(){
	var ctx = document.getElementById('CO2Chart');
	var chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: [],
			datasets: [
			{
				label: "",
				data: [],
				borderColor: 'rgb(0, 105, 217)',
				backgroundColor: 'rgba(0, 105, 217, 0.2)'
			}
			]
		},
		options: {
			title: {
				display: true,
				text: 'CO2'
			}
		}
	});
	console.log('CO2Chart was built');
	return chart;
}

window.pressureChart = new function buildPressure(){
	var ctx = document.getElementById('pressureChart');
	var chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: [],
			datasets: [{
				label: "",
				data: [],
				borderColor: 'rgb(0, 105, 217)',
				backgroundColor: 'rgba(0, 105, 217, 0.2)'
			}]
		},
		options: {
			title: {
				display: true,
				text: 'Pressure'
			}
		}
	});
	console.log('pressureChart was built')
	return chart;
}


function addData(data){
	document.getElementById('pressureVal').innerText = `Pressure:${data.pressure}`
	document.getElementById('temperature1Val').innerText = `Pressure:${data.temperature[0]}`
	document.getElementById('temperature2Val').innerText = `Pressure:${data.temperature[1]}`
	document.getElementById('humidityVal').innerText = `Pressure:${data.humidity}`
	document.getElementById('CO2Val').innerText = `Pressure:${data.CO2}`
	fire_el = document.getElementById('fire');
	if(data.fire == true && fire_el.getAttribute('active') == 'false'){
		fire_el.src = '/static/pictures/fire_active.png';
		fire_el.setAttribute('active', 'true');
	}
	if(data.fire == false && fire_el.getAttribute('active') == 'true'){
		fire_el.src = '/static/pictures/fire.png';
		fire_el.setAttribute('active', 'false');
	}
	for(var sensor in data){
		if(sensor == 'fire')
			continue;
		var chart = window[sensor + 'Chart'];
		
		if(!(data[sensor] instanceof Array))
			data[sensor] = [data[sensor]];
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
			if(data[sensor][i] == -1.0 && chart.data.datasets[i].label != 'Error') {
				chart.data.datasets[i].oldLabel = chart.data.datasets[i].label;
				chart.data.datasets[i].oldColor = chart.data.datasets[i].borderColor; 
				console.log(chart.data.datasets[i].oldLabel, chart.data.datasets[i].oldColor);
				//chart.data.datasets[i].oldBackgroundColor = chart.data.datasets[i].backgroundColor; 
				chart.data.datasets[i].borderColor = 'rgb(255, 0, 0)';
				//chart.data.datasets[i].backgroundColor = 'rgba(255, 0, 0, 1)'
				chart.data.datasets[i].label = 'Error';
				continue;
			} else if(chart.data.datasets[i].label =='Error' && data[sensor][i] != -1.0) {
				chart.data.datasets[i].label = chart.data.datasets[i].oldLabel;
				chart.data.datasets[i].borderColor = chart.data.datasets[i].oldColor;
			} else if (chart.data.datasets[i].label =='Error' && data[sensor][i] == -1.0) {
				continue;
			}
			chart.data.datasets[i].data[chart.data.labels.length - 1] = data[sensor][i];
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

function checkLogin(){
	console.log({password: $('#password')[0].value});
	$.post({
		url: 'checkLogin',
		data: {password: $('#password')[0].value},
		success: function(result){
			if(result == 'True')
				window.location.href = "/getAdmin";
		}
	})
}

function startDevice(device){
	console.log(`${device}`);
	$.post({
		url: '/startDevice',
		data: {sensor: device},
		success: function(result){
			if(result == 'Error')
				return
			d = document.getElementById(device);
			d.checked = result;
			console.log(`${device}:${d.checked}`);
		}
	})
}


function updateAll(){
	getInfo()
	camera = document.getElementById('camera');
	camera.src = "state.jpg";
}

timer = setInterval(updateAll, 1000);