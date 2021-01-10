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
    stations.setAll(collection);
  }
  else
  {
    stations.clearAll();
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

stations.getAll = function()
{
  return stations.collection;
}

stations.setAll = function(collection)
{
  stations.collection = collection;
  write();
}

stations.clearAll = function()
{
  stations.setAll({});
}
