#!/usr/bin/env python

import boto3  
import json
import os, sys
import image
import re
import thread
import requests

def replace_element(lst, new_element, indices):
	for i in indices:
		lst[i] = new_element
	return lst

def sendRequest(url, paramas):
    r = requests.post(url, data=paramas)
    print(r)

def imageRekogniser(imageurl):

	f = open("{}".format(imageurl))
	# rek = boto3.client('rekognition')
	# readfile = f.read()
	rek = boto3.client('rekognition', region_name='us-west-2', aws_access_key_id="AKIAJGF5VFUKW2HXEEUA", aws_secret_access_key="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")
	readfile = f.read()
	results2 = rek.detect_faces(  
	    Image={
	        'Bytes': readfile
	    },
	    Attributes=[
	    'ALL',
	]
	)

	jsonDatastring = json.dumps(results2['FaceDetails'], indent=2)
	jsonData = json.loads(jsonDatastring)

	if len(jsonData) == 0:
		results3 = rek.detect_labels(  
		    Image={
		        'Bytes': readfile
		    },
		    MaxLabels=15,
	    	MinConfidence=60
		)

		objectsDictionaryArray = []
		jsonData2 = json.dumps(results3, indent=2)
		newData2 = json.loads(jsonData2)
		objects = newData2["Labels"]

		for i in objects:
			nameOfObject = i.get("Name")
			objectsDictionaryArray.append(nameOfObject)
		jointString = ', '.join(objectsDictionaryArray[:len(objectsDictionaryArray)-1])
		lastElement = '{}'.format(objectsDictionaryArray[len(objectsDictionaryArray)-1])
		print("Your environment contains a {} and a {}".format(jointString, lastElement))
			
	else:

		jsonDataa = json.dumps(results2['FaceDetails'][0], indent=2)
		newData = json.loads(jsonDataa)
		emotions = newData["Emotions"]
		gender = newData["Gender"]

		HighageRange = newData["AgeRange"]["High"]
		LowageRange = newData["AgeRange"]["Low"]
		averageAge = (HighageRange+LowageRange)/2
		everyemotionArray = []
		genderArray = []
		genderArray.append(gender)

		for i in emotions:
			everyemotionArray.append(i)

		singleEmotion = everyemotionArray[0]
		conf = singleEmotion["Confidence"]

		valueofgender = genderArray[0]
		conf2 = valueofgender["Value"]

		n = conf*0.01
		emotion = ""


		if singleEmotion["Type"] == "SAD" or singleEmotion["Type"] == "CONFUSED" or singleEmotion["Type"] == "ANGRY" or singleEmotion["Type"] == "DISGUSTED":
			emotion = singleEmotion["Type"]
			print((1/n)-1)
		elif singleEmotion["Type"] == "HAPPY" or  singleEmotion["Type"] == "SURPRISED" or singleEmotion["Type"] == "CALM":
			emotion = singleEmotion["Type"]
			print(n)
		else:
			print(0.5)

		results3 = rek.detect_labels(  
		    Image={
		        'Bytes': readfile
		    },
		    MaxLabels=10,
	    	MinConfidence=60
		)

		lowercaseemotion = emotion.lower()

		objectsDictionaryArray = []
		jsonData2 = json.dumps(results3, indent=2)
		newData2 = json.loads(jsonData2)
		objects = newData2["Labels"]

		for i in objects:
			nameOfObject = i.get("Name")
			objectsDictionaryArray.append(nameOfObject)

		traits = ', '.join(objectsDictionaryArray[2:3])
		moretraits = ','.join(objectsDictionaryArray[3:len(objectsDictionaryArray)-2])
		lastElement = '{}'.format(objectsDictionaryArray[len(objectsDictionaryArray)-1])

		bigstring = ("Your environment contains a {} {} with {}, {} and an average age of {} with {} gender. ".format(lowercaseemotion, traits, moretraits, lastElement, averageAge, conf2))
		print(bigstring)
		print(jsonDataa)
  #       sendRequest('http://178.62.14.170:4242/capture', {'valence': n, 'finalString': bigstring})

if __name__ == '__main__':

	methodname = sys.argv[1]
	imageRekogniser(methodname)



