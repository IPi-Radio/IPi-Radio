const stations = require("../stations");

const api = module.exports = {};

api.attach = function(app)
{
  app.get("/api/stations/all", function (req, res) {
    res.send(stations.getAll());
  });

  app.post("/api/stations/clear", function (req, res) {
    stations.clearAll();
    res.send("OK");
  });

  app.post("/api/stations/set", function (req, res) {
    stations.setAll(req.body);
    res.send("OK");
  });

  app.post("/api/stations/remove", function (req, res) {
    let name = req.param("name");
    if (stations.remove(name) == false)
    {
      res.status(204); // no content
    }
    res.send("OK");
  });

}
