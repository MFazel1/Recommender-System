# Recommender-System


This project using instagram tags for recommending the most recent events to the user by using anoumaly detection technique. The idea is if the number of occurences of the tag within the specific time is very low, it is most probable that there is a new event is going on. To do that, the user inputs the tag name that they want to learn informastion about it. we named it input tag. Then the system will collect other tags (Secondary tag) associated with the input tag and stores them in DB along with the post time on Instagram. Then the systsm starts finding the correlation between input tag and secondary tags within the time granularity of minutes, hours and days. The computed results will store in DB for further access. 
 

# Project Components
The anomaly project consists of three main components; Tags_collection, Fetch_data and rate_value.
  - Tags_Collection : This component is in charge of collecting tags from Instagram by using APIGEE
framework and store in the DB. The information that we are using is Tag ID, Input Tag,
Secondary Tag, number of occurrences of the tag and the time when the tag was
posted. We wrote a recursive function and set the time in the way that the script fetches
the information from the Instagram API each 30 seconds automatically and updates the
DB. If there was no new information it waits for the next time slot. In order to be sure than no data overlapping occurs we defined the ID list and before adding into file, it checks if the new ID is not already existed in the ID pools. Then the
new line will be written to the file.
  - Fetch_data: Fetching data is responsible to set an anomaly rate to each secondary tag based on its
population in DB. We tested multiple complicated queries on the data to have a better resultion regarding to the data. For example in the Fetch_data.py, there is a querry to rate the tags
where the input tags is assigned by user and one step further we also consider the time
when the hours ranging between 9-10 am. We can rate the tags on the time granularity of second, minute,
hours, day, month and year. And this is very interesting because the anomaly output will
be filtered based on the time range. Moreover for double checked we added the tags to
the python_like_dictionary type by using “mbd.cursors.Dictcursor” to ignore overlapping. Then we normalaized the rate by using the maximum and minimum of the output and then calculate the rate functions. 


                                                        F(x)=x-min/max-min

By using this function, using max value will return 1 and min returns 0 which is the maximum value for anomaly. At the end we can get the anomaly rate value by entering Input tag and secondary tag. Our approach has the advantage of detecting anomalies by specifying time fractions. In more detail, we can detect the anomaly rate for the secondary tag within seconds, hours, days, months and years ranges. For example we can find out what is the anomaly rate of fashion as secondary tag and newyork as an input tag between 10-12 am or on Mondays or weekdays or in February and so on. To be simplified we defined a simple function to rate the tags.And at the end the out put will be stored in DB.

  - Rate_value: This component is in charge of printing the rate values based on the user query.



