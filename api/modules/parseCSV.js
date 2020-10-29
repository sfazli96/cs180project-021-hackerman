var fs = require('fs');


function parseCSV(filepath) {
	var file = fs.readFileSync(filepath, 'utf8');
    var rows = file.split('\n');
    var data = {};
    
    // Create list of headers
    var headers = rows[0].split(',');
    
    // Create keys using headers in JSON object
    for(var i = 0; i <= headers.length-1; i++) {
    	var header = headers[i].split(',');
    	header = header[0].split('\r');
    	// Creating JSON with keys as headers
    	data[header[0]] = [];
    }
    // Current Problem is I cannot split each row by ','
    // Must find another way to split each row.
    for(var i = 1; i <= rows.length-2; i++){
    	// Grab single row to splut
    	var row = parseLine(rows[i]);

    	data['video_id'].push(row[0]);
    	data['trending_date'].push(row[1]);
    	data['title'].push(row[2]);
    	data['channel_title'].push(row[3]);
    	data['category_id'].push(row[4]);
    	data['publish_time'].push(row[5]);
    	if(row[6] != '[none]') {
    		var tags = row[6].split('|');
    		data['tags'].push(tags);
    	}
    	else {
    		data['tags'].push([]);
    	}
    	data['views'].push(row[7]);
    	data['likes'].push(row[8]);
    	data['dislikes'].push(row[9]);
    	data['comment_count'].push(row[10]);
    	data['thumbnail_link'].push(row[11]);
    	data['comments_disabled'].push(row[12]);
    	data['ratings_disabled'].push(row[13]);
    	data['video_error_or_removed'].push(row[14]);
    	data['description'].push(row[15]);
    }

    return data;
}

function parseLine(line) {

	var parsedLine = [];
	var quotes = false;
	var tags = false;
	var cell = '';
	var i = 0;
	while(i <= line.length){
		if(tags && line.charAt(i)==','){
			tags = false;
			parsedLine.push(cell);
			cell = '';
		}
		else if(tags){
			cell += line.charAt(i);
		}
		else if(line.charAt(i)=='"' && quotes){
			quotes = false;
			if(i == line.length-2){
				parsedLine.push(cell);
				cell = '';
			}
			else if(i == line.length-1){
				parsedLine.push('');
			}
		}
		else if(quotes) {
			cell += line.charAt(i);
		}
		else if(line.charAt(i)=='"' && !quotes){
			quotes = true;
		}
		else if(line.charAt(i)==','){
			if(line.indexOf('000Z') == (i-4)){
				parsedLine.push(cell);
				cell = '';
				tags = true;
			}
			else if(tags){
				tags = false;
			}
			else{
				parsedLine.push(cell);
				cell = '';				
			}
		}
		else{
			cell += line.charAt(i);
		}
		i+=1;
	}
	return parsedLine;
}

// Save the data structure as a JSON file
function saveJSON(filename, data){
	var jsonDATA = JSON.stringify(data);
	fs.writeFile(`${filename}.txt`, jsonDATA, function(err) {
		if(err){
			console.log(err);
		}
	});
}

// const filepath = '../data/USvideos.csv';
// var data = parseCSV(filepath);
// saveJSON( 'USVideos', data);

module.exports = {
	parseCSV: parseCSV,
	saveJSON: saveJSON,
};