from .helpers import *
from hackerman import urls
import json
from collections import Counter
import pathlib

# Changes category_id from csv to a string
# Example: 22 -> 'Entertainment'
def categories_to_names(category, country):
	# Open json file specific to the country csv file.
	# The {} in the file name gets replaced with 'US' or 'GB', etc
	# with open('/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/{}_category_id.json'.format(country)) as f:
	with open(pathlib.Path(__file__).parent/'data/{}_category_id.json'.format(country)) as f:
		# category_names is dictionary now
		category_names = json.load(f)

	# Iterate through json file until you've found the category ID passed in
	for item in category_names['items']:
		if category == item['id']:
			#print('In categories_to_names', type(item['id']))
			f.close()

			# This return should look something like:
			# item['snippet']['title'] => 'Entertainment'
			return item['snippet']['title']
			

# # Get various modified data on each video
# def video_info():
# 	# Make dictionary with video_ids
# 	videos = {}

# 	# Iterate through every country to get comment counts and
# 	# various other information on each video
# 	for country in urls.global_data.keys():
# 		# Create empty dictionary for each country
# 		# Will look like: {'US': {'28x7aysd7': {'comment_count': 123, 'thumbnail': 'https://asdjwhihasd.com', ...}}}
# 		videos[country] = {}
# 		for index, ID in enumerate(urls.global_data[country]['video_id']):
# 			if ID not in videos[country].keys():
# 				videos[country][ID] = {}
# 				videos[country][ID]['trending_dates'] = []

# 			videos[country][ID]['comment_count'] = urls.global_data[country]['comment_count'][index]
# 			videos[country][ID]['thumbnail_link'] = urls.global_data[country]['thumbnail_link'][index]
# 			videos[country][ID]['title'] = urls.global_data[country]['title'][index]

# 			# Modify publish time for easier calculations
# 			# Looks like (year, day, month)
# 			publish_time = parseDate(urls.global_data[country]['publish_time'][index])
# 			videos[country][ID]['published_date'] = publish_time
# 			videos[country][ID]['trending_dates'].append(urls.global_data[country]['trending_date'][index])
# 			videos[country][ID]['category'] = categories_to_names(urls.global_data[country]['category_id'][index], country)
# 			videos[country][ID]['likes'] = urls.global_data[country]['likes'][index]
# 			videos[country][ID]['dislikes'] = urls.global_data[country]['dislikes'][index]
# 			videos[country][ID]['views'] = urls.global_data[country]['views'][index]

# 	return videos

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
				response[names[value]
				    ]['likes'][0] += int(urls.global_data['US']['likes'][i])
				response[names[value]]['likes'][1] += 1
			if urls.global_data['US']['dislikes'][i]:
				response[names[value]
				    ]['dislikes'][0] += int(urls.global_data['US']['dislikes'][i])
				response[names[value]]['dislikes'][1] += 1
			if urls.global_data['US']['views'][i]:
				response[names[value]
				    ]['views'][0] += int(urls.global_data['US']['views'][i])
				response[names[value]]['views'][1] += 1

	# This dictionary will hold all numbers used to plot the graph
	analyze_this = {}

	# Go through the categories to average likes/dislikes/views
	for cat in categories:
		likes_num = response[names[cat]]['likes'][0]
		likes_den = response[names[cat]]['likes'][1]
		#avg_likes = likes_num/likes_den

		dislikes_num = response[names[cat]]['dislikes'][0]
		dislikes_den = response[names[cat]]['dislikes'][1]
		#avg_dislikes = dislikes_num/dislikes_den

		views_num = response[names[cat]]['views'][0]
		views_den = response[names[cat]]['views'][1]   
		#avg_views = views_num/views_den

		# Finally set this value to each category
		analyze_this[names[cat]] = {'avg_likes': {'numerator': likes_num, 'denominator': likes_den},
		    'avg_dislikes': {'numerator': dislikes_num, 'denominator': dislikes_den}, 'avg_views': {'numerator': views_num, 'denominator': views_den}}

	return analyze_this

def top_20_most_liked(country):
	# Create two lists: one for the keys, and one for the values
	list_titles = list(urls.global_data[country]['title'])
	list_likes = list(urls.global_data[country]['likes'])

	# Create an empty dictionary for the above two lists
	twentyMostLiked = {}
	top20mostliked = {}

	# Convert the likes list values into integers
	for i in range(0, len(list_likes)):
		list_likes[i] = int(list_likes[i])

	# Another way of putting both lists into a dictionary file
	twentyMostLiked = {list_titles[i]: list_likes[i]
	    for i in range(len(list_titles))}

	# Sort the dictionary from most to least likes, and then push the top 20 results into another dictionary file
	k = Counter(twentyMostLiked)
	top20mostliked = dict(k.most_common(20))

	return top20mostliked

def top_20_most_disliked(country):
	# Create two lists: one for the keys, and one for the values
	list_titles = list(urls.global_data[country]['title'])
	list_dislikes = list(urls.global_data[country]['dislikes'])

	# Create an empty dictionary for the above two lists
	twentyMostDisliked = {}
	top20mostdisliked = {}

	# Convert the dislikes list values into integers
	for i in range(0, len(list_dislikes)):
		list_dislikes[i] = int(list_dislikes[i])

	# Another way of putting both lists into a dictionary file
	twentyMostDisliked = {list_titles[i]: list_dislikes[i]
	    for i in range(len(list_titles))}

	# Sort the dictionary from most to least dislikes, and then push the top 20 results into another dictionary file
	k = Counter(twentyMostDisliked)
	top20mostdisliked = dict(k.most_common(20))

	return top20mostdisliked

def disabled(num):
	if num == 1:
		thisDict = {}
		thisDict = disabled_comments()
		return thisDict
	else:
		thatDict = {}
		thatDict = disabled_ratings()
		return thatDict

def disabled_comments():
	disabled_comments_US = 0
	disabled_comments_CA = 0
	disabled_comments_GB = 0
	disabled_comments_DE = 0

	# Disabled comments sections for each country
	# Append the status of all comments sections for each country into their own list
	list_disabled_comments_US = list(urls.global_data['US']['comments_disabled'])
	list_disabled_comments_CA = list(urls.global_data['CA']['comments_disabled'])
	list_disabled_comments_GB = list(urls.global_data['GB']['comments_disabled'])
	list_disabled_comments_DE = list(urls.global_data['DE']['comments_disabled'])

	# Loop through all the videos with disabled comments
	# For every instance of a video with a disabled comments section, increment a counter
	# United States
	for i in range(0, len(list_disabled_comments_US)):
		if list_disabled_comments_US[i] == 'True':
			disabled_comments_US += 1
	# Canada
	for i in range(0, len(list_disabled_comments_CA)):
		if list_disabled_comments_CA[i] == 'True':
			disabled_comments_CA += 1
	# Great Britain
	for i in range(0, len(list_disabled_comments_GB)):
		if list_disabled_comments_GB[i] == 'True':
			disabled_comments_GB += 1
	# Germany
	for i in range(0, len(list_disabled_comments_DE)):
		if list_disabled_comments_DE[i] == 'True':
			disabled_comments_DE += 1

	all_disabled_comments_vids = { 'United States' : disabled_comments_US, 'Canada' : disabled_comments_CA, 'Great Britain' : disabled_comments_GB, 'Germany' : disabled_comments_DE }

	# Sort dictionary from most comments-disabled videos to least
	all_disabled_comments_vids = Counter(all_disabled_comments_vids)
	return all_disabled_comments_vids

def disabled_ratings():
	disabled_ratings_US = 0
	disabled_ratings_CA = 0
	disabled_ratings_GB = 0
	disabled_ratings_DE = 0

	list_disabled_ratings_US = list(urls.global_data['US']['ratings_disabled'])
	list_disabled_ratings_CA = list(urls.global_data['CA']['ratings_disabled'])
	list_disabled_ratings_GB = list(urls.global_data['GB']['ratings_disabled'])
	list_disabled_ratings_DE = list(urls.global_data['DE']['ratings_disabled'])

	for i in range(0, len(list_disabled_ratings_US)):
		if list_disabled_ratings_US[i] == 'True':
			disabled_ratings_US += 1

	for i in range(0, len(list_disabled_ratings_CA)):
		if list_disabled_ratings_CA[i] == 'True':
			disabled_ratings_CA += 1
	
	for i in range(0, len(list_disabled_ratings_GB)):
		if list_disabled_ratings_GB[i] == 'True':
			disabled_ratings_GB += 1

	for i in range(0, len(list_disabled_ratings_DE)):
		if list_disabled_ratings_DE[i] == 'True':
			disabled_ratings_DE += 1

	all_disabled_ratings_vids = { 'United States' : disabled_ratings_US, 'Canada' : disabled_ratings_CA, 'Great Britain' : disabled_ratings_GB, 'Germany' : disabled_ratings_DE }
	all_disabled_ratings_vids = Counter(all_disabled_ratings_vids)
	return all_disabled_ratings_vids

# filepath = '/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/USvideos.csv'
# avg_per_cat(filepath)

def most_popular_categories(country_name):
	response = {}
	names = {}

	# Make list of unique category ID values
	# categories looks liks this:
	# categories = [1, 15, 22, 25, ...]
	categories = list(set(urls.global_data[country_name]['category_id']))

	# Initialize names and response dictionaries
	for cat in categories:
		# Convert category ID to string
		name = categories_to_names(cat, country_name)

		# names looks like:
		# {22: 'Entertainment', 24: 'Gaming', ...}
		names[cat] = name

		# resposne looks like:
		# {'Entertainment': {'views': [0, 0]}, ...}
		response[name] = {'views': [0, 0]}

	# Iterate through category IDs, and enumerate to have index
	for i, value in enumerate(urls.global_data[country_name]['category_id']):
		if value:
			# If the views entry exists and is not null
			if urls.global_data[country_name]['views'][i]:
				# Then record the data into the response dictionary
				response[names[value]]['views'][0] += int(urls.global_data[country_name]['views'][i])
				response[names[value]]['views'][1] += 1

	analyze_this = {}

    # Go through the categories to average likes/dislikes/views
	for cat in categories:
		video_views = response[names[cat]]['views'][0]
		analyze_this[names[cat]] = {'video_views' : video_views}

	return analyze_this

def most_active_comments(country):
	# Create two lists: one for the keys, and one for the values
	list_titles = list(urls.global_data[country]['title'])
	list_comment_count = list(urls.global_data[country]['comment_count'])

	# Create an empty dictionary for the above two lists
	twentyFiveMostLiked = {}
	top25MostLiked = {}

	# Convert the comment_count list values into integers
	for i in range(0, len(list_comment_count)):
		list_comment_count[i] = int(list_comment_count[i])

	# Another way of putting both lists into a dictionary file
	twentyFiveMostLiked = {list_titles[i]: list_comment_count[i]
	    for i in range(len(list_titles))}

	# Sort the dictionary from most to least comment_count, and then push the top 20 results into another dictionary file
	k = Counter(twentyFiveMostLiked)
	top25MostLiked = dict(k.most_common(25))

	return top25MostLiked

# Get various modified data on each video
# DONT WORRY ABOUT THIS CODE:
# def video_info():
# 	# Make dictionary with video_ids
# 	videos = {}

# 	# Iterate through every country to get comment counts and
# 	# various other information on each video
# 	for country in global_data.keys():
# 		# Create empty dictionary for each country
# 		videos[country] = {}
# 		for index, ID in enumerate(global_data[country]['video_id']):
# 			if index == 0:
# 				videos[country][ID] = {}
# 				videos[country][ID]['comment_count'] = []
# 			# Looks like: {'US': {'28x7aysd7': {'comment_count': [123, 123, 123, ...], 'thumbnail': 'asdjwhihasd.com', ...}}}
# 			videos[country][ID]['comment_count'].append(global_data[country]['comment_count'][index])
# 			videos[country][ID]['thumbnail_link'] = global_data[country]['thumbnail_link'][index]
# 			videos[country][ID]['title'] = global_data[country]['title'][index]
# 			# Modify publish time to look like trending date
# 			# So, from 2017-11-10T17:00:03.000Z to 17.10.11
# 			publish_time = parseDate(global_data[country]['publish_time'][index])
# 			break
# 			videos[country][ID]['published_date'] = publish_time

#video_info()

# def comment_count_per_country():
# 	# counts looks like:
# 	# {'US': {'total_comments': 1242512, 'average_comments': 5000}}
# 	counts = {}
# 	for country in videos.keys():
# 		counts[country] = {}
# 		counts[country]['total_comments'] = 0
# 		counts[country]['average_comments'] = 0
# 		for ID in videos[country].keys():
# 			counts[country]['total_comments'] += int(videos[country][ID]['comment_count'])
# 		counts[country]['average_comments'] = counts[country]['total_comments']/len(videos[country].keys())

# 	return counts

# Grab top 5 trending length videos for each country
# def trending_stats():
# 	# time looks like:
# 	# {'US': {'18dja98s': {'trending_length': 1, 'time_to_trend': 1, 'thumbnail_link': 'https://aasidh.com'}, ...}, ...}
# 	top5 = {}
# 	time = {}
# 	for country in videos.keys():
# 		time[country] = {}
# 		for ID in videos[country].keys():
# 			time[country][ID] = {}
# 			if len(videos[country][ID]['trending_dates']) > 0:
# 				time[country][ID]['first_trend'] = videos[country][ID]['trending_dates'][0]
# 				time[country][ID]['first_published'] = videos[country][ID]['publish_time']
# 				time[country][ID]['trending_length'] = trendingLength(videos[country][ID]['trending_dates'])
# 				time[country][ID]['time_to_trend'] = timeToTrend(videos[country][ID]['trending_dates'], videos[country][ID]['published_date'])
# 				time[country][ID]['thumbnail_link'] = videos[country][ID]['thumbnail_link']
# 			else:
# 				time[country][ID]['first_trend'] = ''
# 				time[country][ID]['first_published'] = ''
# 				time[country][ID]['trending_length'] = 0
# 				time[country][ID]['time_to_trend'] = 0
# 				time[country][ID]['thumbnail_link'] = ''
# 		top5[country] = {}
# 		top5[country]['top_trending'] = topTrending(time[country])

# 	# DO TOP 5 CALCULATIONS HERE
# 	return time