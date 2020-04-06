#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:06:42 2020

@author: firozshaikh
"""

#title           :ITunesAPI.py
#description     :Designed to extract track lising and albums data for 
#                 Itunes music artists
#author          :Firoz Shaikh
#date            :20200406
#version         :0.1
#usage           :python pyscript.py
#notes           :
#python_version  :3.7.0  
#==============================================================================


# Import packages
import requests
import sys
from datetime import datetime


#define 
class ITunesTrack:
    
        def __init__(self):
            # The ITunes URL
            self.url = "https://itunes.apple.com/"
#define the URL where we do the artist search            
        def urlTrack(self):
            global url1
            artNm.replace(" ","")
            url1 = self.url  + "search?term=" + artNm + \
                "&country=GB&music=musicTrack&limit=" + str(limit)
            return url1
#method for sending a request to the API and capturing the response
        def Request(self):
            global json_data
            self.urlTrack()
            r = requests.get(url1)
            if r.status_code == 200:
                json_data = r.json()
            else:
               print("API non responsive, exiting program...")
               sys.exit()
            return json_data

#the method for processing the json data in python  
        def json_music(self,msctype):
            self.Request()
#need to know the number of results pulled so we can loop through them            
            l= json_data['resultCount']
            if l ==0:
                print("No items to display")
                sys.exit()   
            n=0
            cat = {}
            #NB any duplicates pairs added to the dictionary will be deduped
            #extract track name and release date
            for j in range(l):
                for p in json_data['results'][j].keys():
                 if p == msctype:
                     tr = json_data['results'][j][msctype]
                     re = json_data['results'][j]["releaseDate"][:10]
                     cat.update({tr:re})
                     n +=1
            #if we cant find any tracks
            if n ==0:
                print("No items to display")
                sys.exit()   
                
            #sort the albums by release date
            sort_cat = dict(sorted(cat.items(), key=lambda x: 
                                 datetime.strptime(x[1], '%Y-%m-%d'), 
                                 reverse=True))
                
            #print the latest tracks from the artist
            for k in sort_cat.keys():
                print(k)
                print("ReleaseDate" + ': ', sort_cat[k],"\n")   
#get the artist name and id from the json data                 
        def id(self):
            global artid,artist
            self.Request()
            artid = ""
            artist = ""
            if "artistId" in json_data['results'][0]:
                artid =  json_data['results'][0]["artistId"]   
            if "artistName" in json_data["results"][0]:
                artist = json_data["results"][0]["artistName"]
            return artid,artist

#define a class for the URl if an albums search is required
class ITunesAlbum(ITunesTrack):
        
    def urlAlbum(self):
        global url1
        url1 = self.url + "lookup?id=" + str(artid) \
            + "&entity=album" \
                + "&limit=" + str(limit)
        return url1

#start program and request data from user

print("**************Search Artists Using The ITunes API**************")

artNm = ""
#ask for a search term
q = len(artNm)
while len(artNm) == 0:
    try:
        artNm = input("\nPlease type artist to search: ")
        if len(artNm) == 0:
            print("No search text was entered")
            raise ValueError
#ask for more than 1 character to restrict search results            
        elif len(artNm) == 1:
            print("Please enter more than 1 character")
            raise ValueError
    except ValueError:
        print("Appropriate search characters not entered")
        sys.exit()     
    except:
        print("an unexpected error has occured")
        sys.exit() 
        

#ask for the number of records to display    
#NB. We may search for 20 records but when we process them they are duplicates
#(despite having differing track IDs)
#these will be duduped so 20 records my not display        
limit=0
while limit ==0:   
    try:
        limit = int(input("\nType number of records to search for(1 to 200): "))
        if limit > 200 or limit < 0:
            print("Number entered was not in range 1-200, default of 20 used")
            limit = 50
    except ValueError:   
        print("Number between 1 and 200 not entered, try again")
        limit = 0    
    except:
        print("unexpected error occured")
        sys.exit()
    else:
#call the methods for displaying the tracks
        a = ITunesTrack()
#the id method is needed for getting the artist so we can use the print below        
        a.id()
        print("\n**********Tracks for",artist, "**********\n")
        a.json_music("trackName")
             
#check if displaying the albums if required        
albm = ""          
while albm == "":
    try:
        albm = input("Do you wish to display albums (Y/N?): ").upper()
        print(albm)
        if albm not in ["Y","N"]:
            raise ValueError
    except ValueError:
        print("Y or N was not input. Please try again")
        albm = ""
    except:
        print("an unexpected error occured")
    else:
        if albm == "Y":
#call the methods for printing the album            
            print("**********Albums for",artist,"**********\n")       
            b = ITunesAlbum()
            b.urlAlbum()
            b.json_music("collectionName") 
        elif albm == "N":
            print("Program ending")
            sys.exit()
        
        
