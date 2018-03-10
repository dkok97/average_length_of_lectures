import json
import time
import csv
from pprint import pprint

majors = {}

data = json.load(open('Fall2017.json'))

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

i=0
total_lec_length=0.0
total_number_of_days=0
no_of_lectures=0.0
while (i!=len(data)):
    major_name = str(data[i]['fields']['subject'])
    majors[major_name]=[]
    curr_major=major_name
    while (major_name==curr_major and i!=len(data)):
        day_times=data[i]['fields']['day_times']
        if (day_times==""):
            i+=1
        elif (day_times[0]=='M' or day_times[0]=='T' or day_times[0]=='W' or day_times[0]=='R' or day_times[0]=='F'):
            times = get_lectures_disc(day_times)
            time_diff, no_of_days=get_lecture_length(times[0])
            total_lec_length+=time_diff
            total_number_of_days+=no_of_days
            no_of_lectures+=1
            i+=1
        else:
            i+=1
        if i < len(data):
            curr_major = str(data[i]['fields']['subject'])
    if (total_lec_length==0):
        del majors[major_name]
        total_number_of_days=0
        no_of_lectures=0.0
        continue
    majors[major_name].append(total_lec_length/no_of_lectures)
    majors[major_name].append(total_number_of_days/no_of_lectures)
    total_lec_length=0.0
    total_number_of_days=0
    no_of_lectures=0.0

with open('Fall2017-lectures.csv', 'wb') as csvfile:
    lec_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    lec_writer.writerow(['major','average lecture time (one day)','average num of days a week', 'average lecture time (one week)'])
    lec_writer.writerow(['','','', ''])
    for n,l in majors.items():
        lec_writer.writerow([n,round(l[0],2),round(l[1],2), round(l[0]*l[1],2)])
print majors
