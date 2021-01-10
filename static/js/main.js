// prototype improvements

Array.prototype.remove = function(item) {
    for (let i = 0; i < this.length; i++) {
        if (this[i] === item) {
            this.splice(i, 1);
        }
    }
}

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
  entry.html.remove();
  $("#stations").accordion("refresh");


  // remove from internal collectio
  stations.remove(entry);
}

function generateHtml(entry)
{
  let html = entry.html = $("<div class=\"station\">");

  // title
  html.append("<h3>"+entry.name+"</h3>");

  // info container
  let container = $("<div>");
  html.append(container);
  container.append("<p>url: "+entry.url+"</p>");
  container.append("<p>time: "+entry.time+"</p>");

  // delete button
  let deleteButton = $(`
    <button class="stationDeleteButton">
      <span class="ui-icon ui-icon-closethick"></span>
    </button>
    `);
  deleteButton.button();
  deleteButton.click(function()
  {
    removeEntry(entry);
  });
  container.append(deleteButton);

  return html;
}

// initialization

$(function()
{
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
});
