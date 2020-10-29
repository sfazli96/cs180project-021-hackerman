var express = require('express');
var router = express.Router();
var parse = require('../modules/parseCSV.js');


const testRoute = (app, fs) => {
	const data = parse.parseCSV('./data/USvideos.csv');
	
	app.get('/test', (req, res) => {
		res.json(data['title']);
	});

}




// router.get('/', function(req, res, next) {
//     res.json(['A', 'B', 'C']);
// });

module.exports = testRoute;