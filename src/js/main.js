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
let searchResult = [];

// Methods

function checkButton(id)
{
	var new_name = $(id).val();
	$("#addRadioName").prop("disabled", new_name.length < 1);
}

function checkTime(input)
{
	// const regex = /^[0-2][0-9]:[0-5][0-9](\s-\s[0-2][0-9]:[0-5][0-9])?$/;
	const regex = /^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]((\s-\s|-)([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9])?$/;

	if (regex.test($(input).val()) || $(input).val() === "")
	{
		$(input).css("color", "");
		$("#saveStationOrder").prop("disabled", false);
	}else
	{
		$(input).css("color", "red");
		$("#saveStationOrder").prop("disabled", true);
	}
}

function checkNewName(input, entry)
{
	let valid = true;
	let newName = $(input).val();

	// check if name is unique
	$(".acc-header").each(function()
	{
		if ($(this).html() === newName && newName != $("h3", entry.html).find(".acc-header").html())
		{
			valid = false;
		}
	});

	// check if name is empty
	if (!newName)
	{
		valid = false;
	}

	if (valid)
	{
		$(input).css("color", "");
		$("#saveStationOrder").prop("disabled", false);
	} else
	{
		$(input).css("color", "red");
		$("#saveStationOrder").prop("disabled", true);
	}

	return valid
}

function updateName(input_element, entry)
{
	new_name = input_element.val();

	$(entry.html).attr("name", new_name);
	$("h3", entry.html).find(".acc-header").html(new_name);

	$("#stations").accordion("refresh");
}

// Search functions
function searchByName()
{
	// http://all.api.radio-browser.info/json/stations/byname/{searchterm}

	rName = $("#radioStatioName").val();
	console.log(rName);

	$.get("http://all.api.radio-browser.info/json/stations/byname/"+encodeURIComponent(rName), function(data)
	{
		console.log(data);
		// clear search result array
		searchResult = [];
		$(".resultItem").remove();

		for (const [key, value] of Object.entries(data))
		{
			let entry = value;
			entry.html = generateResultItem(entry);
			searchResult.push(entry);

			$("#resultList").append(entry.html);
		}
	});
}

function generateResultItem(entry)
{
	let html = $(`<button type="button" class="list-group-item list-group-item-action resultItem" name="${searchResult.length}" onclick="addEntry(this)">`);
	let stationInfo = entry.name
		+" | codec: "+entry.codec
		+" | bitrate: "+entry.bitrate
		+" | countrycode: "+entry.countrycode+" "+entry.state
		+" | lang: "+entry.language
		+" | clicks: "+entry.clickcount;

	html.append(stationInfo);

	return html;
}

function addEntry(entry)
{
	//console.log(entry);
	//console.log(entry.name);
	//console.log(searchResult[entry.name]);

	let newEntry = searchResult[entry.name];
	newEntry.time = "";
	newEntry.url = newEntry.url_resolved;

	// check entries using the same name (name has to be unique)
	stations.forEach(function(item)
	{
		if (item.name === newEntry.name)
		{
			newEntry.name += "_";
		}
	});

	newEntry.html = generateHtml(newEntry);
	stations.push(newEntry);

	// append
	$("#stations").append(newEntry.html);
	$("#stations").accordion("refresh");

	/*
	$.post("/api/stations/add", JSON.stringify(newEntry) , function(data)
	{
		console.log("add station: "+data);
	});
	*/
}

function removeEntry(entry)
{
	/*
	// send api request
	$.post("/api/stations/remove/"+encodeURIComponent(entry.name), function(data)
	{
		console.log("remove station: "+data);
	});
	*/

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
	$.post("/api/stations/clear", function(data)
	{
		console.log("clear all stations: "+data);
	});

	// elements
	$("#stations").remove();
	$("#stations").accordion("refresh");
}

function pushAllEntries()
{
	// workaround for some cyclic error bug whatever the fuck
	let tmp_stations = stations;

	tmp_stations.forEach(function(item)
	{
		delete item.html;
	});

	//console.log(JSON.stringify(stations));

	$.post("/api/stations/saveall", JSON.stringify(stations), function(data)
	{
		console.log("update all stations: "+data);
		if (data == "OK")
		{
			alert("Saving successful!");
		}
	})
}

function entryGenerator(label, value, disabled)
{
	let entry = $('<div class="input-group mb-3">');
	let labelHtml = $('<div class="input-group-prepend">');

	let classes = "form-control radio-property"

	// add placeholder for the time field
	switch (label) {
		case "time":
			var addon = 'placeholder="hh:mm[ - hh:mm]" onkeyup="checkTime(this)"';
			break;
	
		default:
			var addon = "";
			break;
	}

	if (disabled)
	{
		var valueHtml = $(`<input class="${classes}" type="text" name="${label}" value="${value}" ${addon} disabled />`);
	} else
	{
		var valueHtml = $(`<input class="${classes}" type="text" name="${label}" value="${value}" ${addon} />`);
	}
	
	// put all together
	labelHtml.append(`<span class="input-group-text">${label}</span>`);
	entry.append(labelHtml);
	entry.append(valueHtml);

	return entry;
}

function generateHtml(entry)
{
	let html = entry.html = $(`<div class="sortable-item station" name="${entry.name}">`);

	// title
	html.append(`<h3><span class="acc-header">${entry.name}</span></h3>`);

	// info container
	let container = $("<div>");
	html.append(container);
	/* container.append(`<p>time: ${entry.time}</p>`); */
	nameEntry = entryGenerator("name", entry.name, false)
	container.append( nameEntry );
	container.append( entryGenerator("time", entry.time, false) );
	container.append( entryGenerator("url", entry.url, false) );
	container.append( entryGenerator("codec", entry.codec, true) );
	container.append( entryGenerator("bitrate", entry.bitrate, true) );
	container.append( entryGenerator("countrycode", entry.countrycode, true) );
	container.append( entryGenerator("language", entry.language, true) );

	// name change event
	nameEntry.keyup(function()
	{
		input_element = $(".radio-property", this);

		if (checkNewName(input_element, entry))
		{
			updateName(input_element, entry);
		}
	});

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

function getEntriesOrder()
{
	let listData = [];

	$(".station").each(function()
	{
		listData.push($(this).attr("name"));
	});

	console.log(listData);
	generateHtml(newEntry);
}

function updateOrder()
{
	let newOrder = [];

	// fetch current order
	$(".station").each(function()
	{
		let currName = $(this).attr("name");

		stations.forEach(function(item)
		{
			if (item.name === currName)
			{
				//console.log("FOUND: "+ item.name);
				newOrder.push(item);
			}
		});
	});

	//console.log(stations);
	//console.log(newOrder);

	stations = newOrder;
}

function updateRadiolist()
{
	let newList = [];

	$(".station").each(function()
	{
		let newEntry = {};

		newEntry["name"] = $(this).attr("name");

		$(this).find(".radio-property").each(function()
		{
			//console.log($(this).attr("name") + ": " + $(this).val());
			newEntry[$(this).attr("name")] = $(this).val();
		});

		newList.push(newEntry);
	});

	console.log(newList);

	stations = newList;
}


// initialization

$(document).ready( function()
{
	// Jquery UI setup
	$("#stations").accordion({ header: "> div.station > h3", active: false, collapsible: true });
	// setup draggable list
	$("#stations")
		.sortable(
		{
			opacity: 0.35
		})
		.disableSelection();

	// init buttons
	$("#clearAllStationsNew").click(function()
	{
		$("#clearAllStationsDialog").show("slow");

		$("#clearAllStationsNO").click(function()
		{
			$("#clearAllStationsDialog").hide("slow");
		});

		$("#clearAllStationsYES").click(function()
		{
			clearAllEntries();
			$("#clearAllStationsDialog").hide("slow");
		});
	});

	$("#addNewStation").click(function()
	{
		$("#newStationFormHead").toggle("slow");
		$("#newStationForm").toggle("slow");
		$("#resultList").toggle();
	});

	$("#saveStationOrder").click(function()
	{
		updateRadiolist();
		/* updateOrder(); */
		pushAllEntries();
	});

	// request all stations
	$.post("/api/stations/all", function(data)
	{
		//console.log(data);

		// collection
		for (const [key, value] of Object.entries(data))
		{
			let entry = value;
			entry.name = key;
			entry.html = generateHtml(entry);
			stations.push(entry);

			// append
			$("#stations").append(entry.html);
		}

		$("#stations").accordion("refresh");
	}, "json");

	// show website
	$("body").fadeIn({
		speed: "fast"
	});
});
