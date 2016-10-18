import requests
import json
import sys
import sched, time
import csv
import datetime
import pymysql
import csvTools
import sys
import MySQLdb
from decimal import Decimal
import MySQLdb as mdb
import sys

#Fetching data from DB and calculating the Rate value
#usage python Fetch_data.py Input tage
#sample usage "python Fetch_data.py newyork
Secondary_List={}
Input_Time={}
try:
	con = mdb.connect(host='localhost', port=3306, user='root', passwd='****', db='Anomaly');
	con.autocommit(True)
	#cur = con.cursor()
	cur = con.cursor(mdb.cursors.DictCursor)
	#cur.execute("SELECT * FROM Tag_info WHERE Input_Tag= '%s' AND Secondory_Tag!= '%s' ORDER BY Occurrence_number DESC LIMIT 10000" % ('newyork','newyork'))
	#cur.execute("SELECT S.Input_Tag, S.Secondory_Tag, C.Occurrence_number FROM Tag_info S INNER JOIN (SELECT Secondory_Tag, count(Secondory_Tag) as cnt FROM Tag_info GROUP BY Secondory_Tag)\
	# C ON S.Secondory_Tag = C.Secondory_Tag LIMIT 100")
	#Count occurrences of distinct values
	#cur.execute("SELECT Secondory_Tag, count(*) AS occurrences FROM Tag_info GROUP BY Secondory_Tag ORDER BY occurrences DESC, Secondory_Tag")
	#count vs time changes
	#cur.execute("SELECT Input_Tag,Secondory_Tag, Time,COUNT(Secondory_Tag) FROM Tag_info WHERE  HOUR(Time) BETWEEN 9 AND 10 GROUP BY Secondory_Tag, HOUR(Time) \
	#			HAVING COUNT(Secondory_Tag)>1 ORDER BY COUNT(Secondory_Tag)  ")
	cur.execute("SELECT Input_Tag, Secondory_Tag, Time,COUNT(Secondory_Tag) FROM Tag_info WHERE Input_Tag='%s' AND HOUR(Time) BETWEEN 9 AND 10 GROUP BY Secondory_Tag, HOUR(Time) \
				HAVING COUNT(Secondory_Tag)>1 ORDER BY COUNT(Secondory_Tag) " % (sys.argv[1]))
	# Last Query
	#cur.execute("SELECT Input_Tag,Secondory_Tag, Time,COUNT(Secondory_Tag) FROM Tag_info WHERE Input_Tag= '%s' AND Secondory_Tag= '%s' AND HOUR(Time) BETWEEN '%s' AND '%s' GROUP BY Secondory_Tag, Time \
	#			HAVING COUNT(Secondory_Tag)>1 ORDER BY COUNT(Secondory_Tag)" % (str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4])))
	#Max valuye of each secondary input
	#cur.execute("SELECT Input_Tag,Secondory_Tag, Time, max(Secondory_Tag) AS max FROM Tag_info WHERE  HOUR(Time) BETWEEN 9 AND 10 GROUP BY Secondory_Tag, MINUTE(Time) \
	#			HAVING COUNT(Secondory_Tag)>1 ORDER BY max(Secondory_Tag)")	
	#SELECT name,COUNT(*) as count FROM tablename GROUP BY name ORDER BY count DESC;
	rows = cur.fetchall() 	
	for row in rows:
		#if i!=0:
			#print row
			j+=1
			#
			if row["Secondory_Tag"] not in Secondary_List.keys():
				Secondary_List[row["Secondory_Tag"]] = row["COUNT(Secondory_Tag)"]
				Input_Time[row["Input_Tag"]]=row["Time"]
				#print row["Secondory_Tag"], row["Occurrence_number"]
				#print row
				
			else:
				if(Secondary_List[row["Secondory_Tag"]]<=row["COUNT(Secondory_Tag)"]):
					Secondary_List[row["Secondory_Tag"]]=row["COUNT(Secondory_Tag)"]					
					
					
	#find max and min value of Ocuurance #
	#for key in Secondary_List.keys():
	#	print key
	#print max(Secondary_List.keys(), key=Secondary_List.get)
	#input("max")
	#print Secondary_List
	#print max(Secondary_List.keys(), key=int)
	#input("max")
	#print min(Secondary_List.keys(), key=int)
	#input("min")
	first=True
	Max=0
	Min=0
	Items = sorted(Secondary_List,key=Secondary_List.get,reverse=True)
	#print Items
	for item in Items:
		if(first):
			print item ,Secondary_List[item]
			Max=Secondary_List[item]
			first=False
			
		else:
			Min=Secondary_List[item]
			
	print Max,Min
	
	#input("max and min")
	#Rate function F(x)=x-min/max-min	
	#Insert Rate into the table
	for item in Items:
			print Secondary_List[item],Min,Max
			rate= (Decimal(Secondary_List[item]-Min))/(Decimal(Max-Min))
			print "rate:%.2f",rate
			#input("rate")
			#print "Row is:%s",row["Id"],row["#input_Tag"],row["Secondary_Tag"],row["Occurrence_number"],row["Time\r"]
			#print
			#'#input Tag', 'Secondary Tag' , 'Occurrence number', 'Time'
			#"INSERT INTO Test (lat,lng,LocationID,CreatedTime) VALUES ('%s','%s','%s','%s')" % (row["lat"],row["lng"],row["Location ID"],row["Created Time\r"])
			try:
				query = "INSERT IGNORE INTO Rate_Value (input_Tag,Secondory_Tag,Rate,Time) VALUES ('%s','%s','%s','%s')" % (sys.argv[1],item,str(rate),"1-1-1")
				cur.execute(query)
			except MySQLdb.Error, e:
				print "An error has been passed. %s" %e
				##input("salam")
				
			#input("inserted")
	'''for key, value in Secondary_List.items() :
		print (key, value)
		'''
					
			
				
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
	#print j ,z       
	if con:    
		con.close()

		