from difflib import SequenceMatcher
from hackerman import urls

def loadCSV(countries):
	# Load up CSV so that it's available to all
	country_dict = {}
	for country in countries:
		filepath = '/mnt/d/Documents/UC-Riverside/Fall-2020/CS180/Class-Projects/cs180project-021-hackerman/mysite/client/data/{}videos.csv'.format(country)
		print('Loading up {} CSV file...'.format(country))
		country_dict[country] = parseCSV(filepath)
		print('Finished loading up {}'.format(country))
	return country_dict

# Parse CSV files with these helper function
def parseCSV(filepath):
	with open(filepath, newline='\n') as rows:
		data = {}   
		headers = rows.readline().split(',')

		data['video_id'] = []
		data['trending_date'] = []
		data['title'] = []
		data['channel_title'] = []
		data['category_id'] = []
		data['publish_time'] = []
		data['tags'] = []
		data['views'] = []
		data['likes'] = []
		data['dislikes'] = []
		data['comment_count'] = []
		data['thumbnail_link'] = []
		data['comments_disabled'] = []
		data['ratings_disabled'] = []
		data['video_error_or_removed'] = []
		data['description'] = []

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
			if row[15]:
				data['description'].append(row[15])
			else:
				data['description'].append('')
		rows.close()
	return data

def parseLine(line):
	parsedLine = []
	quotes = False
	tags = False
	cell = ''
	i = 0
	#print('_________________ NEW LINE HERE _____________')
	while (i < len(line)):
		if tags and line[i]==',':
			tags = False
			#print(cell, '|||||||||||')
			parsedLine.append(cell)
			cell = ''
		elif tags:
			cell += line[i]
		elif line[i]=='"' and quotes:
			quotes = False
			if i == len(line)-3:
				#print(cell, '|||||||||||')
				parsedLine.append(cell)
				cell = ''
			elif i == len(line)-2:
				#print(cell, '|||||||||||')
				parsedLine.append('')
		elif quotes:
			cell += line[i]
		elif line[i]=='"' and not quotes:
			quotes = True
		elif line[i]==',':
			# Grab index of this substring
			if line.find('000Z') == (i-4):
				#print(cell, '|||||||||||')
				parsedLine.append(cell)
				cell = ''
				tags = True
			elif tags:
				tags = False
			else:
				#print(cell, '|||||||||||')
				parsedLine.append(cell)
				cell = ''
		else:
			cell += line[i]
		i+=1
	# if len(parsedLine) > 16 or len(parsedLine) < 16:
	# 	print('Somet fucked')
	#print(len(parsedLine))
	return parsedLine;

def searchCSV(query, country):
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

	for i, j in enumerate(urls.global_data[country]['channel_title']):
		if SequenceMatcher(lambda x: x=='', j, query['channel_title']).ratio() > 0.6:
			if query['video_id'] or query['publish_time'] or query['category_id'] or query['tags']:
				if query['video_id'] == urls.global_data[country]['video_id'][i]:
					indices_of_queries.append(i)
				elif query['publish_time'] == urls.global_data[country]['publish_time'][i]:
					indices_of_queries.append(i)
				elif query['category_id'] == urls.global_data[country]['category_id'][i]:
					indices_of_queries.append(i)
				elif query['tags'] in urls.global_data[country]['tags'][i]:
					indices_of_queries.append(i)
			else:
				indices_of_queries.append(i)

	for index in list(set(indices_of_queries)):
		response['video_id'].append(urls.global_data[country]['video_id'][index])
		response['channel_title'].append(urls.global_data[country]['channel_title'][index])
		response['publish_time'].append(urls.global_data[country]['publish_time'][index][:10])
		response['category_id'].append(urls.global_data[country]['category_id'][index])
		response['trending_date'].append(urls.global_data[country]['trending_date'][index])
		response['views'].append(urls.global_data[country]['views'][index])
		response['likes'].append(urls.global_data[country]['likes'][index])
		response['dislikes'].append(urls.global_data[country]['dislikes'][index])
		response['comment_count'].append(urls.global_data[country]['comment_count'][index])

	return response

def parseDate(date):
	split_date = date.split('T')

	print(split_date)
	new_date = split_date[0][2:].replace('-', '.')
	print(new_date)
	month = new_date[3:5]
	day = new_date[6:8]
	print(month, day)
	new_date = new_date.replace(month, day)
	new_date = new_date.replace(day, month)
	print(new_date)
