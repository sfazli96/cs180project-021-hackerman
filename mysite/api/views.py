from django.shortcuts import render

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


#data = parseCSV('data/USvideos.csv')