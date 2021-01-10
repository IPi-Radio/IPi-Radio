const path = require("path");

// Stations
const stations = require("./stations");
stations.initialize(path.resolve(__dirname, "../stations.json"));

// Server
const Server = require("./server");
const server = new Server();
server.listen();
