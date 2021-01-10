const stations = require("../stations");

const api = module.exports = {};

api.attach = function(app)
{
  app.get("/api/stations/all", function (req, res) {
    res.send(stations.getAllStations());
  });

  app.post("/api/stations/clear", function (req, res) {
    stations.clearAllStations();
    res.send("OK");
  });

  app.post("/api/stations/set", function (req, res) {
    stations.setAllStations(req.body);
    res.send("OK");
  });

}
