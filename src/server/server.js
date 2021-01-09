const express = require("express");
const api = require("./api.js");

module.exports = class Server
{
	constructor()
	{
		this.app = express();
    this.app.use(express.static("./static"));
    api.attach(this.app);
	}

  listen()
  {
    this.app.listen(8080);
  }
}
