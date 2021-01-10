// Jquery UI setup

$(function(){
  $("#stations").accordion({ header: "> div.station > h3", active: false, collapsible: true });
});

$(".widget input[type=submit], .widget a, .widget button").button();

 $("button, input, a").click(function(event)
 {
   event.preventDefault();
 });

// State variables

let collection = [];

// methods

function addEntry(entry)
{

}

function removeEntry(name)
{

}

// initialization

$.get("/api/stations/all", function(data)
{
  for (const [key, value] of Object.entries(data))
  {
    // row
    let row = $("<div class=\"station\">");

    // title
    row.append("<h3>"+value.name+"</h3>");

    // info container
    let container = $("<div>");
    row.append(container);
    container.append("<p>url: "+value.url+"</p>");
    container.append("<p>time: "+value.time+"</p>");

    // delete button
    let deleteButton = $(`
      <button class="stationDeleteButton">
        <span class="ui-icon ui-icon-closethick"></span>
      </button>
      `);
    deleteButton.button();
    container.append(deleteButton);

    // append
    $("#stations").append(row);
  }

  $("#stations").accordion("refresh");

});
