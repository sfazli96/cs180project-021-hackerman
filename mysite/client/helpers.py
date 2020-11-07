from difflib import SequenceMatcher
from hackerman import urls

def loadCSV(filepath):
	# Load up CSV so that it's available to all
	return parseCSV(filepath)

# Parse CSV files with these helper function
def parseCSV(filepath):
	with open(filepath, newline='\n') as rows:
		data = {}   
		headers = rows.readline().split(',')
		# Get headers
		for header in headers:
			header = header.split('\r\n')
			data[header[0]] = []

		for row in rows.readlines():
			#print(row)
			row = parseLine(row);
			data['video_id'].append(row[0])
			data['trending_date'].append(row[1])
			data['title'].append(row[2])
			data['channel_title'].append(row[3])
			data['category_id'].append(row[4])
			data['publish_time'].append(row[5])
			if row[6] != '[none]':
				tags = row[6].split('|')
				data['tags'].append(tags)
			else:
				data['tags'].append([])
			data['views'].append(row[7])
			data['likes'].append(row[8])
			data['dislikes'].append(row[9])
			data['comment_count'].append(row[10])
			data['thumbnail_link'].append(row[11])
			data['comments_disabled'].append(row[12])
			data['ratings_disabled'].append(row[13])
			data['video_error_or_removed'].append(row[14])
			data['description'].append(row[15])
		rows.close()
	print(len(data['likes']))
	return data

def parseLine(line):
	parsedLine = []
	quotes = False
	tags = False
	cell = ''
	i = 0
	while (i < len(line)):
		if tags and line[i]==',':
			tags = False
			parsedLine.append(cell)
			cell = ''
		elif tags:
			cell += line[i]
		elif line[i]=='"' and quotes:
			quotes = False
			if i == len(line)-3:
				parsedLine.append(cell)
				cell = ''
			elif i == len(line)-2:
				parsedLine.append('')
		elif quotes:
			cell += line[i]
		elif line[i]=='"' and not quotes:
			quotes = True
		elif line[i]==',':
			# Grab index of this substring
			if line.find('000Z') == (i-4):
				parsedLine.append(cell)
				cell = ''
				tags = True
			elif tags:
				tags = False
			else:
				parsedLine.append(cell)
				cell = ''
		else:
			cell += line[i]
		i+=1
	# if len(parsedLine) > 16 or len(parsedLine) < 16:
	# 	print('Somet fucked')

	return parsedLine;

def searchCSV(query):
	# Send in data as dictionary from POST
	# Search parsed CSV file for these values
	#data = global_data
	response = {}
	response['video_id'] = []
	response['channel_title'] = []
	response['publish_time'] = []
	response['category_id'] = []
	response['trending_date'] = []
	response['views'] = []
	response['likes'] = []
	response['dislikes'] = []
	response['comment_count'] = []
	indices_of_queries = []

	for i, j in enumerate(urls.global_data['channel_title']):
		if SequenceMatcher(lambda x: x=='', j, query['channel_title']).ratio() > 0.6:
			if query['video_id'] or query['publish_time'] or query['category_id'] or query['tags']:
				if query['video_id'] == urls.global_data['video_id'][i]:
					indices_of_queries.append(i)
				elif query['publish_time'] == urls.global_data['publish_time'][i]:
					indices_of_queries.append(i)
				elif query['category_id'] == urls.global_data['category_id'][i]:
					indices_of_queries.append(i)
				elif query['tags'] in urls.global_data['tags'][i]:
					indices_of_queries.append(i)
			else:
				indices_of_queries.append(i)

	for index in list(set(indices_of_queries)):
		response['video_id'].append(urls.global_data['video_id'][index])
		response['channel_title'].append(urls.global_data['channel_title'][index])
		response['publish_time'].append(urls.global_data['publish_time'][index][:10])
		response['category_id'].append(urls.global_data['category_id'][index])
		response['trending_date'].append(urls.global_data['trending_date'][index])
		response['views'].append(urls.global_data['views'][index])
		response['likes'].append(urls.global_data['likes'][index])
		response['dislikes'].append(urls.global_data['dislikes'][index])
		response['comment_count'].append(urls.global_data['comment_count'][index])

	return response
