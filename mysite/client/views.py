from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from client.serializers import UnitedStatesSerializer
from rest_framework import status


# Create your views here.
def US(request):
	return render(request, 'US.html', {})

def home(request):
	return render(request, 'home.html', {})

class UnitedStatesView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'US.html'

	def get(self, request):
		# Seems like I do something like this:
		YTdata = [{"video_id":'1238xxase12h8as', "channel_title": 'Fucker', "trending_date": '2017-01-01', 'category': 22, 'tags': 'Fuck'}]
		serializer = UnitedStatesSerializer(YTdata, many=True)
		return Response({'serializer': serializer, 'data': YTdata})

	def post(self, request):
		#YTdata = [{"video_id":'1238xxase12h8as', "channel_title": 'Fucker', "trending_date": '2017-01-01', 'category': 22, 'tags': 'Fuck'}]
		serializer = UnitedStatesSerializer(data=request.data)
		if not serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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

# TODO
# Get a simple POST to work
# Then get a GET request to work
# NOTE: You can pass in data into the Serializers as a list of dictionaries.
#       So, when you manage to get data to GET request, you can make it a list