from difflib import SequenceMatcher
from datetime import date
from hackerman import urls
from .analytics import categories_to_names
import pathlib
from google_drive_downloader import GoogleDriveDownloader as gdd
import requests

def loadCSV(countries):
	# First download the CSV and JSON files from Google Drive
	# Downloads a zip file and unzips all CSV and JSON files into a folder called "data"
	# If the folder already exists, it will skip this part
	if not pathlib.Path('client/data/').exists():
		gdd.download_file_from_google_drive(file_id='1xLFbM_pb_-tkcjCQY6IwlyJG1u5M4Qs9',dest_path='client/data/data.zip',unzip=True)
	
	# Load up CSV so that it's available to all
	country_dict = {}
	for country in countries:
		# filepath = '/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/{}videos.csv'.format(country)
		filepath = pathlib.Path(__file__).parent/'data/{}videos.csv'.format(country)
		print('Loading up {} CSV file...'.format(country))
		country_dict[country] = parseCSV(filepath)
		print('Finished loading up {}'.format(country))
	return country_dict

# Parse CSV files with these helper function
def parseCSV(filepath):
	with open(filepath, newline='\n', errors='ignore') as rows:
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

# Parse date that is in a specific format
def parseDate(date):
	split_date = date.split('T')

	new_date = split_date[0][2:].split('-')
	year = new_date[0]
	month = new_date[1]
	day = new_date[2]
	return (year, day, month)

# returns how many days a video was trending
def trendingLength(dates):
	# Get first day of trending
	date_first = dates[0].split('.')
	year_first = int('20' + date_first[0])
	day_first = int(date_first[1])
	month_first = int(date_first[2])

	# Get last day of trending
	date_last = dates[len(dates)-1].split('.')
	year_last = int('20' + date_last[0])
	day_last = int(date_last[1])
	month_last = int(date_last[2])

	f_date = date(year_first, month_first, day_first)
	l_date = date(year_last, month_last, day_last)

	delta = l_date-f_date
	return delta.days+1

# Return amount of days it took to trend from published
def timeToTrend(dates, pub_date):
	first_date = dates[0].split('.')
	# Get first day of trending
	year_first = int('20' + first_date[0])
	day_first = int(first_date[1])
	month_first = int(first_date[2])
	l_date = date(year_first, month_first, day_first)

	p_year = int('20' + pub_date[0])
	p_day = int(pub_date[1])
	p_month = int(pub_date[2])
	f_date = date(p_year, p_month, p_day)

	delta = l_date - f_date

	return delta.days

def insert(data):
	#print('DATA IS:', data)
	urls.global_data[data['country']]['video_id'].append(data['video_id'])
	urls.global_data[data['country']]['trending_date'].append(data['trending_date'])
	urls.global_data[data['country']]['channel_title'].append(data['channel_title'])
	urls.global_data[data['country']]['title'].append(data['title'])
	urls.global_data[data['country']]['category_id'].append(data['category_id'])
	urls.global_data[data['country']]['tags'].append([])
	urls.global_data[data['country']]['publish_time'].append(data['publish_date']+ '17:00:03.000Z')
	urls.global_data[data['country']]['views'].append(data['views'])
	urls.global_data[data['country']]['likes'].append(data['likes'])
	urls.global_data[data['country']]['dislikes'].append(data['dislikes'])
	urls.global_data[data['country']]['comment_count'].append(data['comment_count'])
	urls.global_data[data['country']]['thumbnail_link'].append('')
	urls.global_data[data['country']]['comments_disabled'].append(False)
	urls.global_data[data['country']]['ratings_disabled'].append(False)
	urls.global_data[data['country']]['video_error_or_removed'].append(False)
	urls.global_data[data['country']]['description'].append('')

	# Update averages here:
	cat = str(data['category_id'])
	country = data['country']
	cat_name = categories_to_names(cat, country)

	urls.averages[cat_name]['avg_likes']['numerator'] += int(data['likes'])
	urls.averages[cat_name]['avg_likes']['denominator'] += 1

	urls.averages[cat_name]['avg_dislikes']['numerator'] += int(data['dislikes'])
	urls.averages[cat_name]['avg_dislikes']['denominator'] += 1

	urls.averages[cat_name]['avg_views']['numerator'] += int(data['views'])
	urls.averages[cat_name]['avg_views']['denominator'] += 1

def delete(data):
	#print('DATA IS:', data)
	country = data['country']
	indices_to_delete = []
	for index, value in enumerate(urls.global_data[country]['channel_title']):
		if data['channel_title'] == value:
			cat = str(urls.global_data[country]['category_id'][index])
			urls.averages[categories_to_names(cat, country)]['avg_likes']['numerator'] -= int(urls.global_data[country]['likes'][index])
			urls.averages[categories_to_names(cat, country)]['avg_likes']['denominator'] -= 1

			urls.averages[categories_to_names(cat, country)]['avg_dislikes']['numerator'] -= int(urls.global_data[country]['dislikes'][index])
			urls.averages[categories_to_names(cat, country)]['avg_dislikes']['denominator'] -= 1

			urls.averages[categories_to_names(cat, country)]['avg_views']['numerator'] -= int(urls.global_data[country]['views'][index])
			urls.averages[categories_to_names(cat, country)]['avg_views']['denominator'] -= 1
			del urls.global_data[country]['video_id'][index]
			del urls.global_data[country]['trending_date'][index]
			del urls.global_data[country]['channel_title'][index]
			del urls.global_data[country]['title'][index]
			del urls.global_data[country]['category_id'][index]
			del urls.global_data[country]['tags'][index]
			del urls.global_data[country]['publish_time'][index]
			del urls.global_data[country]['views'][index]
			del urls.global_data[country]['likes'][index]
			del urls.global_data[country]['dislikes'][index]
			del urls.global_data[country]['comment_count'][index]
			del urls.global_data[country]['thumbnail_link'][index]
			del urls.global_data[country]['comments_disabled'][index]
			del urls.global_data[country]['ratings_disabled'][index]
			del urls.global_data[country]['video_error_or_removed'][index]
			del urls.global_data[country]['description'][index]

	print('Deleted this shit.')

def update(data):
	print('DATA IS:', data)

def topTrending(country_dict):
	top5 = {}
	# top5['top_trending'] = []
	# top5['top_published'] = []
	# Input data looks like:
	# {'video_id': {}}
	for video in country_dict.keys():
		print('fuck')