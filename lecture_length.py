import json
import time
import csv
from pprint import pprint

majors = {}

data = json.load(open('/Users/dinkar/Desktop/the_stack/average_length_of_lectures/Spring2018.json'))

def get_length(from_time, to_time):
    if (len(from_time)==1):
        from_time.append('00'+from_time[0][-2:])
        from_time[0]=from_time[0][:-2]

    if (len(to_time)==1):
        to_time.append('00'+to_time[0][-2:])
        to_time[0]=to_time[0][:-2]

    from_time.append(from_time[1][-2:])
    to_time.append(to_time[1][-2:])
    from_time[1]=int(from_time[1][:2])
    to_time[1]=int(to_time[1][:2])
    from_time[0]=int(from_time[0])
    to_time[0]=int(to_time[0])

    if (from_time[2]=='pm' and from_time[0]!=12):
        from_time[0]+=12
    if (to_time[2]=='pm' and to_time[0]!=12):
        to_time[0]+=12

    time_diff=(to_time[0]*60 + to_time[1])-(from_time[0]*60 + from_time[1])
    return time_diff

def get_lecture_length(time_range):
    days=[]
    from_time=""
    to_time=""
    time_and_day=list(time_range)
    for i in time_range:
        if (i.isupper() and (i=='M' or i=='T' or i=='W' or i=='R' or i=='F')):
            days.append(i)
            time_and_day.remove(i)
        if (i=='\n' or i.isdigit()):
            break
    for i in time_range:
        if (i.isspace()):
            time_and_day.remove(i)
    temp = ''.join(time_and_day)
    for i in range (0,len(temp)):
        if (temp[i].isdigit()):
            break
    temp=temp[i:]
    time_range_list=temp.split('-')
    time_range_list=[time_range_list[0], time_range_list[1]]
    for i in range(0,len(time_range_list[1])):
        if (time_range_list[1][i]=='m'):
            break
    time_range_list[1]=time_range_list[1][0:i+1]
    return get_length(time_range_list[0].split(':'), time_range_list[1].split(':')), len(days)

def get_lectures_disc(lec):
    lec_and_disc=lec.split("|")
    lec_and_disc = [str(lec_and_disc[x]) for x in range(len(lec_and_disc))]
    while '*' in lec_and_disc:
        lec_and_disc.remove('*')
    return lec_and_disc

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

i=0
total_lec_length_upper=0.0
total_lec_length_lower=0.0
total_number_of_days_upper=0
total_number_of_days_lower=0
no_of_lectures_upper=0.0
no_of_lectures_lower=0.0
while (i!=len(data)):
    major_name = str(data[i]['fields']['subject'])
    majors[major_name]=[]
    curr_major=major_name
    while (major_name==curr_major and i!=len(data)):
        day_times=data[i]['fields']['day_times']
        if (day_times==""):
            i+=1
        elif (day_times[0]=='M' or day_times[0]=='T' or day_times[0]=='W' or day_times[0]=='R' or day_times[0]=='F'):
            course_num = getCourseNumber(data[i]["pk"].encode('utf-8'))
            times = get_lectures_disc(day_times)
            time_diff, no_of_days=get_lecture_length(times[0])
            if (course_num >= 1 and course_num <= 99):
                total_lec_length_lower+=time_diff
                total_number_of_days_lower+=no_of_days
                no_of_lectures_lower+=1
            elif (course_num >= 100 and course_num <= 199):
                total_lec_length_upper+=time_diff
                total_number_of_days_upper+=no_of_days
                no_of_lectures_upper+=1
            i+=1
        else:
            i+=1
        if i < len(data):
            curr_major = str(data[i]['fields']['subject'])
    for j in range(0,4):
        majors[major_name].append(0)
    if (no_of_lectures_lower!=0):
        majors[major_name][0]=(total_lec_length_lower/no_of_lectures_lower)
        majors[major_name][1]=(total_number_of_days_lower/no_of_lectures_lower)
    if (no_of_lectures_upper!=0):
        majors[major_name][2]=(total_lec_length_upper/no_of_lectures_upper)
        majors[major_name][3]=(total_number_of_days_upper/no_of_lectures_upper)
    total_lec_length_upper=0.0
    total_lec_length_lower=0.0
    total_number_of_days_upper=0
    total_number_of_days_lower=0
    no_of_lectures_upper=0.0
    no_of_lectures_lower=0.0

with open('Spring2018-data.csv', 'wb') as csvfile:
    lec_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    lec_writer.writerow(['major','average lecture time (one day) - lowerdiv','average num of days a week - lowerdiv', 'average lecture time (one week) - lowerdiv', 'average lecture time (one day) - upperdiv','average num of days a week - upperdiv', 'average lecture time (one week) - upperdiv'])
    lec_writer.writerow(['','','','','','',''])
    for n,l in majors.items():
        lec_writer.writerow([n,round(l[0],2), round(l[1],2), round(l[0]*l[1],2), round(l[2],2), round(l[3],2), round(l[2]*l[3],2)])
