print "imports"
import requests
import pandas as pd
import re


print "initializing dataframe columns"
#For now, only the following 7 properties are collected. More data is coming soon
list_categ_id=[]
list_categ_name=[]
list_city=[]
list_country=[]
list_id=[]
list_name=[]
list_members=[]


print "resqests"
#To be able to request, we follow the instruction of the API meetup
# Here we use the method GET /2/groups
#Please refer to: https://www.meetup.com/fr-FR/meetup_api/docs/2/groups/?uri=%2Fmeetup_api%2Fdocs%2F2%2Fgroups%2F

# For now, only Paris is scanned. More cities are coming soon
city="Paris"
country="fr"
# Get your API key. if you dont have it, check: https://secure.meetup.com/fr-FR/meetup_api/key/
api_key= "ENTER YOUR API KEY HERE"
per_page = 200

#count is used to keep track of the number of group collected in each request
#if it is lower than 200, it means we collected ALL the data matching our request
count=200
#borne is used to avoid infinite loop
borne=0

# off is the offset: it is incremented at each iteration to get the following groups
off=0
while count==200 and borne<1000:
	count=0
	offset = off
	params={"sign":"true","country":"fr", "city":city, "radius": 10, "key":api_key, "page":per_page, "offset":offset }
	#We send the GET request, get the answer in a JSON format
	reponse = requests.get("http://api.meetup.com/2/groups",params=params)
	data = reponse.json()

	# parsing  the JSON file
	for group in data["results"]:
		count+=1
		list_id.append(group["id"])
		list_name.append(group["name"])
		list_categ_id.append(group["category"]["id"])
		list_categ_name.append(group["category"]["name"])
		list_city.append(group["city"])
		list_country.append(group["country"])
		list_members.append(group["members"])
		
	borne+=1
	off+=1
	
	#printing the number of requests sent
	if off%5 ==0:
		print "Requests sent:"+str(off)

print "converting to dataframe"	
df=pd.DataFrame()
df["id"]=list_id					#id of the group
df["name"]=list_name				#name of the group 
df["categ_name"]=list_categ_name    #the name of the group category (ex:robots,Big data,Data Science... are groups from the category tech)
df["categ_id"]=list_categ_id        #Id of the category
df["city"]=list_city                #city
df["country"]=list_country          #country
df["member"]=list_members           #Number of members in the group


print "replacing backspace in df.categ_name"
df["categ_name"]=df["categ_name"].apply(lambda x: x.replace("/","_"))
	
print "saving the data"
df["categ_name"]=df["categ_name"].apply(lambda x: x.encode("utf-8"))
df["city"]=df["city"].apply(lambda x: x.encode("utf-8"))
df["name"]=df["name"].apply(lambda x: x.encode("utf-8"))
# directory to adapt to your working environment
directory=r"C:\Users\Youssef\Documents\Data_Science\MyApps"
df.to_csv(directory+"\\data_2.csv",sep=";",index=False)
