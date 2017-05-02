#!flask/bin/python
import codecs
from flask import Flask
from flask import request

app = Flask(__name__)

KeywordPos = []
comaPos = []
appendedList = ""

def keyword_string(globalStr, pos1, pos2):
	middle_str = globalStr[pos1 :pos2]
	first_brace = middle_str.find("\"")
	second_brace = middle_str.find("\"", (first_brace + 1) )
	return middle_str[ (first_brace + 1) : second_brace]

def findWordOccurence(mainStr, word, posList):
	index = 0
	while index < len(mainStr):
		index = mainStr.find(word, index)
		if index == -1:
			break
		posList.append(index)
		index += len(word)

def getComaPos(mainStr, word, wordPosList):
	start = mainStr.find('[', wordPosList)
	end = mainStr.find(']', start)
	linkStr = mainStr[start : end]
#	findWordOccurence(linkStr, ',', comaPos)
#	comaPos.append(len(linkStr))
	return linkStr

def fetchURL(comaPosList, linkString):
	pos = 0
	appendList = ""
	for loop in range (0, len(comaPosList)):
		fetchedLinks = keyword_string(linkString, pos, comaPosList[loop])
		appendList = appendList + fetchedLinks
		if loop < len(comaPosList) - 1:
			appendList = appendList + ", "
		pos = comaPosList[loop]
	del comaPosList[:]
	return appendList

def get_url_params():
    firstName = request.args.get('keyword')
    return firstName

def main(KeyWord):

    global appendedList
    global comaPos
    global KeywordPos
    appendedList = ""
    appendedList = "{\n" + "\"" + KeyWord + "\"" + ": "
    #print ("\n\nWelcome to Keyword Search\n")

    #filepath = raw_input("Enter file Path : ")
    #KeyWord = raw_input("Enter the keyword to Search : ")
    filepath = "/home/pulkit/Desktop/VLABS_Docs/MY_codes/keyword.json"
    myFile = codecs.open(filepath, "r", 'utf-8')
    contents = myFile.read()
    findWordOccurence(contents, KeyWord, KeywordPos)
    KeywordPos.append(len(contents))
    for x in range(0, len(KeywordPos) - 1):
        linkStr = getComaPos(contents, KeyWord, KeywordPos[x])
        appendedList = appendedList + linkStr + "]"
        if x < len(KeywordPos) - 2:
            appendedList = appendedList + ", " + "\n"
    appendedList = appendedList + "\n}"
    #print appendedList  # for Debug
    return appendedList

@app.route("/get_urls")
def index():
    key = request.args['key']
    test  = main(key)
    return test

if __name__ == '__main__':
    app.run(debug=True)
