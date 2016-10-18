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
#usage python Tags_collection.py Input tage
#sample usage: python Tags_collection.py clarksonuniversity

global count
global tags
tags={}
IDs=[]

s = sched.scheduler(time.time, time.sleep)

requests.packages.urllib3.disable_warnings()

def Fetching(sc):
	count=0
	key ='2228213740.1fb234f.a87267e857be4f4f8e4ea0cee36cabaf' 	
	payload = {"access_token":key}
	Is_state=False
	First=True
	first_time=True	
	i=0
	print First	
	with open('user_info'+'_'+sys.argv[1]+'.csv', 'wb') as fp:
		query=""
		a = csv.writer(fp, delimiter=',')
		if(first_time):					
					data1 = [['Id','#input_Tag', 'Secondary_Tag' , 'Occurrence_number', 'Time']]						
					a.writerows(data1)
					first_time=False
		while i < 10:
			  #make the request
			  r = requests.get('https://api.instagram.com/v1/tags/'+sys.argv[1]+'/media/recent',params=payload,verify=False)#make the request
			  #show our rate limit remaining requests
			  #print r.headers['X-Ratelimit-Remaining']
			  #unserialize the response
			  data = json.loads(r.text)
			  #create the data payload for the next page - note we add max_tag_id which comes from the first requests pagination
			  #print data
			  if(data['pagination']):
			  	payload = {"access_token":key,"max_tag_id":data['pagination']['next_max_id']}
			  else:
				break
			  #print data['data'][0]['tags']
			  #iterate over image data nodes (each one is an image)
			  #Created_time=datetime.datetime.now()	
			  for img in data['data']:
				try:
					date =datetime.datetime.fromtimestamp(int(img['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
				except ValueError:        					 
					input ("invalid format")				
				if(First):
					First=False
					#input("First")
					if img['id'] not in IDs: 
						print "1-not in IDs"
						IDs.append(img['id'])
						State=img['id']
						IDs.append(img['id'])
						Id=State
						for tag in img['tags']:
						  if tag not in tags.keys():							
							tags[tag] = 1		

							try:

								data1 = [[str(Id),str(sys.argv[1]),str(tag) , str("0"),str(date)]]
								a.writerows(data1)
								First=False
								
							except ValueError: 
								print "Needs1 to be encoded"				
						  else:
							tags[tag] += 1
							State=img['id']
							IDs.append(img['id'])
							Id=State
							try:
								data1 = [[str(Id),str(sys.argv[1]), str(tag) , str("0"),str(date)]]
								a.writerows(data1)
							except ValueError:
								print "Needs2 to be encoded"
							

				else:			

					if img['id'] not in IDs: 
						print "not in IDs"
						IDs.append(img['id'])


						for tag in img['tags']:
						  if tag not in tags.keys():
							
							tags[tag] = 1
							Id=img['id']

							
							print tag
							try:
								data1 = [[str(Id),str(sys.argv[1]), str(tag) , str("0"),str(date)]]
								a.writerows(data1)
							except ValueError:
								print "Needs3 to be encoded"

						  else:
							
							tags[tag] += 1
							Id=img['id']
							IDs.append(img['id'])
							try:
								data1 = [[str(Id),str(sys.argv[1]), str(tag) , str("0"),str(date)]]
								a.writerows(data1)
							except ValueError:
								print "Needs4 to be encoded"







			  i+=1
		
		
		fp.close()
		
		#sort the tags dict by its values (counts) return keys as a list
		tagwords = sorted(tags,key=tags.get,reverse=True)
		
		counter=1;
		for word in tagwords:
		  if word=="physicianassistantstudent":
			print "found",tags[word]
			#input ("found")
		  if word=="clarksonuniversity":
			print "found",tags[word]
			#input ("foundclar")
		  
		  print word + " - " + str(tags[word])+"\n"
		  print counter
		  counter+=1
		#print State
		#fp.close()
		##input("file")
		header=True
		with open('user_info'+'_'+sys.argv[1]+'.csv', 'r+') as fp:
			with open('user_info'+'_'+sys.argv[1]+str(count)+'.csv', 'w+') as w:
				for line in fp:
					row=line.split(",")
					if header:
						w.write(line)
						header=False
					for word in tagwords:
						if row[2]==word:							
							row[3]=str(tags[word])
							newline=row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]
							w.write(newline)
							
		fp.close()
		w.close()
					
		duplicat_num=0	
		counter=1
		user_info = csvTools.csvToList('user_info'+'_'+sys.argv[1]+str(count)+'.csv')
		for row in user_info:
			
			
			#print "Row is:%s",row["Id"],row["#input_Tag"],row["Secondary_Tag"],row["Occurrence_number"],row["Time\r"]
			#print
			#'#input Tag', 'Secondary Tag' , 'Occurrence number', 'Time'
			#"INSERT INTO Test (lat,lng,LocationID,CreatedTime) VALUES ('%s','%s','%s','%s')" % (row["lat"],row["lng"],row["Location ID"],row["Created Time\r"])
			try:
				
				query+ = "INSERT IGNORE INTO Tag_info (ID,input_Tag,Secondory_Tag,Occurrence_number,Time) VALUES ('%s','%s','%s','%s','%s')" % (row["Id"],row["#input_Tag"],row["Secondary_Tag"],row["Occurrence_number"],row["Time\r"])
				if(countr%1000=0):
					conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='****', db='Anomaly') #setup our credentials
					conn.autocommit(True)
					cur = conn.cursor()
					cur.execute(query)
			except MySQLdb.Error, e:
				print "An error has been passed. %s" %e
				##input("salam")
				duplicat_num+=1	            
		print query
		#cur.execute(query) #set our query
		print(cur.description)	
		print duplicat_num
		#input("dup;icate")
		count+=1
		sc.enter(30, 1, Fetching, (sc,))
		
		#conn.close()

s.enter(30, 1, Fetching, (s,))


s.run()
cur.close()
