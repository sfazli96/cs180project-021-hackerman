const testRoute = require('./testAPI.js');

const appRouter = (app, fs) => {
	app.get('/', (req, res) => {
		res.send('welcome to the development api-server');
	});

	testRoute(app, fs);
};


module.exports = appRouter;