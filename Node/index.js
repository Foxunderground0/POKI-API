var express = require("express");
var app = express();
const fs = require('fs');

app.set("view engine", "ejs");
//app.use(express.static(__dirname + "/public"));

var files_list = []
var filesystem_root = __dirname + "/../Immages/"

const emotion_dict = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"];
const max_loop_count = 100;

fs.readdir(filesystem_root + "display/", (err, files) => {
	files.forEach(file => {
		//console.log(file);
		files_list.push(file);
	});
	console.log(files_list);
});

app.get("/", function (req, res) {
	var ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
	console.log(ip);
	if (req.query.emotion == undefined) {
		var file = files_list[Math.floor(Math.random() * files_list.length)];
		console.log(file)
		res.sendFile("display/" + file, { root: filesystem_root });
	} else {
		txt = req.query.emotion;
		txt = txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
		if (emotion_dict.includes(txt)) {
			var file = files_list[Math.floor(Math.random() * files_list.length)];
			console.log(file)
			var loop_count = 0;
			while (txt != file.split("_")[0]) {
				if (loop_count >= max_loop_count) {
					res.status(501).send("Couldnt find a match");
				} else {
					var file = files_list[Math.floor(Math.random() * files_list.length)];
					loop_count++;
				}
			}
			res.sendFile("display/" + file, { root: filesystem_root });
		} else {
			//console.log("Here")
			res.status(422).send("Invalid Emotion");
		}
	}
});

let port = process.env.PORT || 8081;
var server = app.listen(port, function () {
	var host = server.address().address;
	var port = server.address().port;
	console.log(`Example app listening at http://${host}:${port}`)
});