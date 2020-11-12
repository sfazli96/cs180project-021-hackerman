from .helpers import *
from hackerman import urls
import json
from collections import Counter
#
# countries = ['US', 'GB', 'DE', 'CA']
# global_data = loadCSV(countries)


# Changes category_id from csv to a string
# Example: 22 -> 'Entertainment'
def categories_to_names(category, country):
	# Open json file specific to the country csv file.
	# The {} in the file name gets replaced with 'US' or 'GB', etc
	with open('/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/{}_category_id.json'.format(country)) as f:
		# category_names is dictionary now
		category_names = json.load(f)

	# Iterate through json file until you've found the category ID passed in
	for item in category_names['items']:
		if category == item['id']:
			f.close()

			# This return should look something like:
			# item['snippet']['title'] => 'Entertainment'
			return item['snippet']['title']

# Average likes, dislikes and views per category for the USA.
def avg_per_cat():

	# Create empty dictionaries for data we want
	response = {}
	names = {}

	# Make list of unique category ID values
	# categories looks liks this:
	# categories = [1, 15, 22, 25, ...]
	categories = list(set(urls.global_data['US']['category_id']))

	# Initialize names and response dictionaries
	for cat in categories:
		# Convert category ID to string
		name = categories_to_names(cat, 'US')

		# names looks like:
		# {22: 'Entertainment', 24: 'Gaming', ...}
		names[cat] = name

		# resposne looks like:
		# {'Entertainment': {'likes': [0, 0], 'dislikes': [0, 0], 'views': [0, 0]}, ...}
		response[name] = {'likes': [0, 0], 'dislikes': [0, 0], 'views': [0, 0]}

	# Iterate through category IDs, and enumerate to have index
	for i, value in enumerate(urls.global_data['US']['category_id']):
		if value:
			# If the likes entry exists and is not null
			if urls.global_data['US']['likes'][i]:
				# Then record the data into the response dictionary
				response[names[value]]['likes'][0] += int(urls.global_data['US']['likes'][i])
				response[names[value]]['likes'][1] += 1
			if urls.global_data['US']['dislikes'][i]:
				response[names[value]]['dislikes'][0] += int(urls.global_data['US']['dislikes'][i])
				response[names[value]]['dislikes'][1] += 1
			if urls.global_data['US']['views'][i]:
				response[names[value]]['views'][0] += int(urls.global_data['US']['views'][i])
				response[names[value]]['views'][1] += 1

	# This dictionary will hold all numbers used to plot the graph
	analyze_this = {}

	# Go through the categories to average likes/dislikes/views
	for cat in categories:
		avg_likes = response[names[cat]]['likes'][0]/response[names[cat]]['likes'][1]
		avg_dislikes = response[names[cat]]['dislikes'][0]/response[names[cat]]['dislikes'][1]
		avg_views = response[names[cat]]['views'][0]/response[names[cat]]['views'][1]

		# Finally set this value to each category
		analyze_this[names[cat]] = {'avg_likes': avg_likes, 'avg_dislikes': avg_dislikes, 'avg_views': avg_views}

	return analyze_this

def top_20_most_liked():
	# Create two lists: one for the keys, and one for the values
	list_titles = list(urls.global_data['US']['title'])
	list_likes = list(urls.global_data['US']['likes'])

	# Create an empty dictionary for the above two lists
	twentyMostLiked = {}
	top20mostliked = {}

	# Convert the likes list values into integers
	for i in range(0, len(list_likes)):
		list_likes[i] = int(list_likes[i])

	# One way of putting both lists into a dictionary file
	'''for key in list_titles:
		for value in list_likes:
			twentyMostLiked[key] = value
			list_likes.remove(value)
			break'''
	
	# Another way of putting both lists into a dictionary file
	twentyMostLiked = {list_titles[i]: list_likes[i] for i in range(len(list_titles))}

	# Sort the dictionary from most to least likes, and then push the top 20 results into another dictionary file
	k = Counter(twentyMostLiked)
	top20mostliked = dict(k.most_common(20))

	return top20mostliked


def top_20_most_disliked():
	# Create two lists: one for the keys, and one for the values
	list_titles = list(urls.global_data['US']['title'])
	list_dislikes = list(urls.global_data['US']['dislikes'])

	# Create an empty dictionary for the above two lists
	twentyMostDisliked = {}
	top20mostdisliked = {}

	# Convert the dislikes list values into integers
	for i in range(0, len(list_dislikes)):
		list_dislikes[i] = int(list_dislikes[i])

	# One way of putting both lists into a dictionary file
	'''for key in list_titles:
		for value in list_dislikes:
			twentyMostDisliked[key] = value
			list_dislikes.remove(value)
			break'''
	
	# Another way of putting both lists into a dictionary file
	twentyMostDisliked = {list_titles[i]: list_dislikes[i] for i in range(len(list_titles))}

	# Sort the dictionary from most to least dislikes, and then push the top 20 results into another dictionary file
	k = Counter(twentyMostDisliked)
	top20mostdisliked = dict(k.most_common(20))

	return top20mostdisliked

# Get various modified data on each video
def video_info():
	# Make dictionary with video_ids
	videos = {}

	# Iterate through every country to get comment counts and
	# various other information on each video
	for country in global_data.keys():
		# Create empty dictionary for each country
		# Will look like: {'US': {'28x7aysd7': {'comment_count': 123, 'thumbnail': 'https://asdjwhihasd.com', ...}}}
		videos[country] = {}
		for index, ID in enumerate(global_data[country]['video_id']):
			if ID not in videos[country].keys():
				videos[country][ID] = {}
				videos[country][ID]['trending_dates'] = []

			videos[country][ID]['comment_count'] = global_data[country]['comment_count'][index]
			videos[country][ID]['thumbnail_link'] = global_data[country]['thumbnail_link'][index]
			videos[country][ID]['title'] = global_data[country]['title'][index]

			# Modify publish time for easier calculations
			# Looks like (year, day, month)
			publish_time = parseDate(global_data[country]['publish_time'][index])
			videos[country][ID]['published_date'] = publish_time
			videos[country][ID]['trending_dates'].append(global_data[country]['trending_date'][index])
			videos[country][ID]['category'] = categories_to_names(global_data[country]['category_id'][index], country)
			videos[country][ID]['likes'] = global_data[country]['likes'][index]
			videos[country][ID]['dislikes'] = global_data[country]['dislikes'][index]
			videos[country][ID]['views'] = global_data[country]['views'][index]

	return videos


def comment_count_per_country(videos):
	# counts looks like:
	# {'US': {'total_comments': 1242512, 'average_comments': 5000}}
	counts = {}
	for country in videos.keys():
		counts[country] = {}
		counts[country]['total_comments'] = 0
		counts[country]['average_comments'] = 0
		for ID in videos[country].keys():
			counts[country]['total_comments'] += int(videos[country][ID]['comment_count'])
		counts[country]['average_comments'] = counts[country]['total_comments']/len(videos[country].keys())

	return counts

# Grab top 5 trending length videos for each country
def trending_stats(videos):
	# time looks like:
	# {'US': {'18dja98s': {'trending_length': 1, 'time_to_trend': 1, 'thumbnail_link': 'https://aasidh.com'}, ...}, ...}
	time = {}
	for country in videos.keys():
		time[country] = {}
		for ID in videos[country].keys():
			time[country][ID] = {}
			if len(videos[country][ID]['trending_dates']) > 0:
				time[country][ID]['trending_length'] = trendingLength(videos[country][ID]['trending_dates'])
				time[country][ID]['time_to_trend'] = timeToTrend(videos[country][ID]['trending_dates'], videos[country][ID]['published_date'])
				time[country][ID]['thumbnail_link'] = videos[country][ID]['thumbnail_link']
			else:
				time[country][ID]['trending_length'] = 0
				time[country][ID]['time_to_trend'] = 0
				time[country][ID]['thumbnail_link'] = ''
	return time
