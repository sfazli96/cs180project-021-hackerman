var express = require('express');
var router = express.Router();

router.get('/sears', function(req, res, next) {
	console.log(req.query);
    res.send(['A', 'B', 'C']);
});

module.exports = router;