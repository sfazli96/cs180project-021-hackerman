const express = require('express')
var path = require('path')
const app = express()
const port = 3000

app.get('/', (request, response) => {
	response.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/', (request, response) => {
	console.log('Sent request! Got status code: %s', response.statusCode);
})

app.listen(port, () => {
	console.log('Example listeing on port ${port}');
});
