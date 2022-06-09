var page = require("webpage").create();

page.open("https://csgostats.gg/player/76561198019779413#/matches", function(status){
    if (status == "success") {
        console.log("The title of the page is: "+ page.title);
        var data = page.content
        console.log(data)

    }page.close();
    phantom.exit();
})
