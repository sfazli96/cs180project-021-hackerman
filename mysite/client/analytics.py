from .helpers import *
from hackerman import urls
import json

def categories_to_names(category):
	with open('/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/US_category_id.json') as f:
		category_names = json.load(f)
	for item in category_names['items']:
		if category == item['id']:
			f.close()
			return item['snippet']['title']

def avg_per_cat():

	response = {}
	names = {}
	categories = list(set(urls.global_data['category_id']))
	for cat in categories:
		name = categories_to_names(cat)
		names[cat] = name
		response[name] = {'likes': [0, 0], 'dislikes': [0, 0], 'views': [0, 0]}

	for i, value in enumerate(urls.global_data['category_id']):
		if value:
			#name = categories_to_names(value)
			if urls.global_data['likes'][i]:
				response[names[value]]['likes'][0] += int(urls.global_data['likes'][i])
				response[names[value]]['likes'][1] += 1
			if urls.global_data['dislikes'][i]:
				response[names[value]]['dislikes'][0] += int(urls.global_data['dislikes'][i])
				response[names[value]]['dislikes'][1] += 1
			if urls.global_data['views'][i]:
				response[names[value]]['views'][0] += int(urls.global_data['views'][i])
				response[names[value]]['views'][1] += 1

	analyze_this = {}

	for cat in categories:
		avg_likes = response[names[cat]]['likes'][0]/response[names[cat]]['likes'][1]
		avg_dislikes = response[names[cat]]['dislikes'][0]/response[names[cat]]['dislikes'][1]
		avg_views = response[names[cat]]['views'][0]/response[names[cat]]['views'][1]
		analyze_this[names[cat]] = {'avg_likes': avg_likes, 'avg_dislikes': avg_dislikes, 'avg_views': avg_views}

	# print(analyze_this)
	return analyze_this


# filepath = '/home/chair/Documents/UCRFall2020/CS180/project/cs180project-021-hackerman/mysite/client/data/USvideos.csv'
# avg_per_cat(filepath)