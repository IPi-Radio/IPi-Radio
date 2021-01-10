const converter = module.exports = {};

converter.toExternal = function(stations)
{
  let external = {};
  for (const [key, value] of Object.entries(stations))
  {
    let station = stations[key];
    let entry = external[station.name] = {};
    entry.url = station.url;
    entry.time = station.time;
  }
  return external;
}

converter.toInternal = function(stations)
{
  let internal = [];
  for (const [key, value] of Object.entries(stations))
  {
    let station = stations[key];
    let entry = {};
    entry.name = key;
    entry.url = station.url;
    entry.time = station.time;
    internal.push(entry);
  }
  return internal;
}
