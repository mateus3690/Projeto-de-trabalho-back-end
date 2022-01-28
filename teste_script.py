from cgi import print_environ


from datetime import datetime

data1 = '2022-01-22 07:50:00'
data2 = '2022-01-22 12:10:00'
data3 = '2022-01-22 12:50:00'
data4 = '2022-01-22 18:03:00'

dataP1 = '08:00:00'
dataP2 = '12:00:00'


s1 = data1.split(' ') #'10:33:26'
s2 = data2.split(' ') #11:15:49' # for example
s3 = data3.split(' ') 
s4 = data4.split(' ')

FMT = '%H:%M:%S'
time1 = datetime.strptime(s2[1], FMT) - datetime.strptime(s1[1], FMT)
print(time1)
timeP = datetime.strptime(dataP2, FMT) - datetime.strptime(dataP1, FMT)
print(timeP)
time1 = str(f'0{time1}')
timeP = str(f'0{timeP}')

time2 = datetime.strptime(time1, FMT) - datetime.strptime(timeP, FMT)


print(time2)
