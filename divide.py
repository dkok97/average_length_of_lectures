import sys
import json

def getCourseNumber(course):
	end = course.find("-") - 1
	#edge case HIN-URD
	if course[end] != ' ':
		end = course.find("-", end + 5) - 1
	start = course.rfind(" ", 0, end - 1)
	val = course[start+1:end]
	courseNum = ''.join(list(filter(lambda x: x.isdigit(), val)))
	if(len(courseNum) == 0):
		return -1
	return int(courseNum)

data = json.load(open('/Users/dinkar/Desktop/the_stack/average_length_of_lectures/Fall2017.json'))
for i in data:
	if (getCourseNumber(i["pk"].encode('utf-8')) <  0):
		print i["pk"].encode('utf-8')
