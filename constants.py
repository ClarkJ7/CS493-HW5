local_url = "http://localhost:8080/"
google_url = "https://intermediate-api-330116.uw.r.appspot.com/"

current_url = "http://localhost:8080/"

boats = "boats"

badMethod = {'Error': "Invalid method for route"}

boatAttr = {'Error': "One or more attributes missing from body of request"}
tooManyAtt = {'Error': "Too many attributes given. Only name, type, and length are accepted"}
boatName = {'Error': "This boat name is already taken"}


invNameChar = {'Error': "Invalid characters used in boat name, only letters or numbers are accepted"}
invNameLen = {'Error': "Too many characters used, maximum length is 20"}

invTypeChar = {'Error': "Invalid characters used in boat name, only letters are accepted"}
invTypeLen = {'Error': "Too many characters used, maximum length is 20"}

invLengthChar = {'Error': "Invalid characters used in boat length, only numbers are accepted"}
invLengthLen = {'Error': "Too many characters used, maximum length is 4"}

boatID = {'Error': "No boat exists with this ID"}