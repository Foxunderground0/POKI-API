var express = require("express");
var app = express();
const fs = require('fs');

app.set("view engine", "ejs");
//app.use(express.static(__dirname + "/public"));

var files_list = []

fs.readdir("Immages/scraped/", (err, files) => {
	files.forEach(file => {
	  //console.log(file);
	  files_list.push(file);
	});
	console.log(files_list);
});

app.get("/", function (req, res) {

	res.sendFile("Immages/scraped/" + files_list[Math.floor(Math.random()*files_list.length)], { root : __dirname/});
});

let port = process.env.PORT || 8081;
var server = app.listen(port, function () {
	var host = server.address().address;
	var port = server.address().port;
	console.log(`Example app listening at http://${host}:${port}`)
});