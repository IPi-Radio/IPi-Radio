
function saveSettings(button)
{
    var formData = $("#settings_form").serializeArray();
    var newData = {};

    for (var i=0; i < formData.length; i++)
    {
        if (formData[i].value.toLowerCase() == "true")
        {
            newData[formData[i].name] = true;
        } else if (formData[i].value.toLowerCase() == "false")
        {
            newData[formData[i].name] = false;
        } else
        {
            newData[formData[i].name] = formData[i].value;
        }
    }

    newData["Port"] = parseInt(newData["Port"]);

    $.post("/api/settings/saveall", JSON.stringify(newData), function(data)
    {
        console.log("update all settings: "+data);

        if (data == "OK")
        {
            alert("Saving successful!");
        }
    })
}

function generateSettingEntry(key, value)
{
    //let html = $('<div class="row">');

	let entry = $('<div class="input-group mb-3">');
	let labelHtml = $('<div class="input-group-prepend">');
    var valueHtml = $(`<input class="form-control" type="text" name="${key}" value="${value}" />`)

    labelHtml.append(`<span class="input-group-text">${key}</span>`);
    entry.append(labelHtml);
    entry.append(valueHtml);

    return entry;
}

function loadSettings()
{
    $.post("/api/settings/all", function(data)
    {
        console.log(data);

        for (const [key, value] of Object.entries(data))
        {
            $("#settings_form").append(generateSettingEntry(key, value));
        }

    }, "json");

    $("#loading").hide();
}

$(document).ready( function()
{
    loadSettings();
});
