// prototype improvements

Array.prototype.remove = function(item) {
		for (let i = 0; i < this.length; i++) {
				if (this[i] === item) {
						this.splice(i, 1);
				}
		}
}

// State variables

let stations = [];

// methods

function addEntry(entry)
{

}

function removeEntry(entry)
{
	// send api request
	$.post("/api/stations/remove/"+encodeURIComponent(entry.name), function(data)
	{
		console.log("remove station: "+data);
	});

	// remove from ui
	$("#stations").accordion(
	{
			active: false,
			collapsible: true
	});
	entry.html.toggle("scale");
	entry.html.fadeOut("slow", function()
	{
		$(this).remove();
		$("#stations").accordion("refresh");
	});


	// remove from internal collection
	stations.remove(entry);
}

function clearAllEntries()
{
	// api
	$.post("/api/stations/clear/", function(data)
	{
		console.log("clear all stations: "+data);
	});

	// elements
	$("#stations").remove();
	$("#stations").accordion("refresh");
}

function getEntriesOrder()
{
	let listData = [];

	$(".station").each(function()
	{
		listData.push($(this).attr("name"));
	});

	console.log(listData);

	return listData;
}

function generateHtml(entry)
{
	let html = entry.html = $('<div class="list-group-item station" name="'+entry.name+'">');

	// title
	html.append("<h3>"+entry.name+"</h3>");

	// info container
	let container = $("<div>");
	html.append(container);
	container.append("<p>time: "+entry.time+"</p>");
	container.append("<p>url: "+entry.url+"</p>");

	// delete button
	let deleteButton = $(`
		<input class="btn btn-danger btn-sm stationDeleteButton" type="button" value="delete" />
	`);
	deleteButton.click(function()
	{
		removeEntry(entry);
	});
	container.append(deleteButton);

	return html;
}

// initialization

$(document).ready( function()
{
	// Jquery UI setup
	$("#stations").accordion({ header: "> div.station > h3", active: false, collapsible: true });
	// setup draggable list
	$("#stations").sortable(
		{
			opacity: 0.35
		})
		.disableSelection();


	$("#clearAllStationsNew").click(function()
	{
		$("#clearAllStationsDialog").show("slow");

		$("#clearAllStationsNO").click(function()
		{
			$(this).parent().parent(".alert").hide("slow");
		});

		$("#clearAllStationsYES").click(function()
		{
			clearAllEntries();
			$(this).parent().parent(".alert").hide("slow");
		});
	});

	// request all stations
	$.get("/api/stations/all", function(data)
	{
		for (const [key, value] of Object.entries(data))
		{
			// collection
			let entry = {};
			entry.name = value.name;
			entry.url = value.url;
			entry.time = value.time;
			entry.html = generateHtml(entry);
			stations.push(entry);

			// append
			$("#stations").append(entry.html);
		}

		$("#stations").accordion("refresh");

	});

	// show website
	$("body").fadeIn({
		speed: "fast"
	});

});
