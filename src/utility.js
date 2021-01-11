const utility = module.exports = {};

utility.requireNotNull = function(value, name)
{
	if (value == null)
	{
		throw new Error(name+" is null");
	}
}

utility.requireType = function(value, name, type)
{
	if (typeof(value) != type)
	{
		throw new Error(name+" is not a "+type);
	}
}

utility.validateStationEntry = function(entry)
{
	utility.requireNotNull(entry.name, "name");
	utility.requireType(entry.name, "name", "string");

	utility.requireNotNull(entry.url, "url");
	utility.requireType(entry.url, "url", "string");

	utility.requireNotNull(entry.time, "time");
	utility.requireType(entry.time, "time", "string");
}
