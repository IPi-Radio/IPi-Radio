const fs = require("fs");
const converter = require("./converter.js");
const utility = require("../utility.js");

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
    stations.setAll(converter.toInternal(collection));
  }
  else
  {
    stations.clearAll();
  }
}

let write = function(commit=true)
{
  if (commit == false)
  {
    return false;
  }
  if (stations.file == null)
  {
    throw new Error("Stations file not initialized");
  }
  let collection = converter.toExternal(stations.collection);
  fs.writeFileSync(stations.file, JSON.stringify(collection, null, 2));
}

stations.getAll = function()
{
  return stations.collection;
}

stations.setAll = function(collection, commit=true)
{
  stations.clear(false);
  stations.addAll(collection, commit);
}

stations.addAll = function(collection, commit=true)
{
  for (let i in collection)
  {
    let station = collection[i];
    stations.add(station, false);
  }

  write(commit);
}

stations.add = function(station, commit=true)
{
  let entry = {};
  entry.name = station.name;
  entry.url = station.url;
  entry.time = station.time;
  utility.validateStationEntry(entry);
  stations.collection.push(entry);

  write(commit);
}

stations.remove = function(name, commit=true)
{
  for (const [key, value] of Object.entries(stations.collection))
  {
    if (value.name === name)
    {
      stations.collection.splice(key, 1);
      write(commit);
      return true;
    }
  }
  return false;
}

stations.clear = function(commit=true)
{
  stations.collection = [];
  write(commit);
}
