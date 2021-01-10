const fs = require("fs");

const stations = module.exports = {};
stations.file = null;
stations.collection = null;

stations.initialize = function(file)
{
  stations.file = file;
  read();
}

let read = function()
{
  if (fs.existsSync(stations.file))
  {
    let data = fs.readFileSync(stations.file);
    let collection = JSON.parse(data);
    stations.setAllStations(collection);
  }
  else
  {
    stations.clearAllStations();
  }
}

let write = function(data)
{
  if (stations.file == null)
  {
    throw new Error("Stations file not initialized");
  }
  fs.writeFileSync(stations.file, JSON.stringify(stations.collection));
}

stations.getAllStations = function()
{
  return stations.collection;
}

stations.setAllStations = function(collection)
{
  stations.collection = collection;
  write();
}

stations.clearAllStations = function()
{
  stations.setAllStations({});
}
