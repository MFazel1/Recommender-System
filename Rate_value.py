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
try:
	con = mdb.connect(host='localhost', port=3306, user='root', passwd='****', db='Anomaly');
	con.autocommit(True)	
	cur = con.cursor()	
	cur.execute("SELECT Rate FROM Rate_Value WHERE Input_Tag= '%s' AND Secondory_Tag='%s' " % (sys.argv[1],sys.argv[2]))	
	rows = cur.fetchall() 
	print rows   
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
	#print j ,z       
	if con:    
		con.close()
