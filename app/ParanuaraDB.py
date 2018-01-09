import json

class ParanuaraDB:
    def loadCompaniesDB(self, companiesDir):
        self.__companiesJson = json.load(open(companiesDir))
        
    def loadPeopleDB(self, peopleDir):
        self.__peopleJson = json.load(open(peopleDir))

#   Creates a map for rapidly access to the names
    def mapNames(self):
        self.__dicCompanyNames = dict()
        self.__dicPeopleNames = dict()
        for idx, val in enumerate(self.__companiesJson):
            self.__dicCompanyNames[self.__companiesJson[idx]["company"]] = idx
        for idx, val in enumerate(self.__peopleJson):
            self.__dicPeopleNames[self.__peopleJson[idx]["name"]] = idx
    
    def getCompanyID(self, companyName):
        if companyName.upper() in self.__dicCompanyNames: # Companies are case-insensitive
            return self.__dicCompanyNames[companyName.upper()]
        else:
            return -1

    def getPersonID(self, name):
        if name in self.__dicPeopleNames:
            return self.__dicPeopleNames[name]
        else:
            return -1
    
    def getNumberOfCompanies(self):
        return len(self.__companiesJson)

    def getNumberOfPeople(self):
        return len(self.__peopleJson)
    
    def getNumberOfMappedPeople(self):
        return len(self.__dicPeopleNames)
    
    def hasCompany(self, companyName):
        return self.getCompanyID(companyName) >= 0
        
    def hasPerson(self, name):
        return self.getPersonID(name) >= 0
        
    def getEmployeesList(self, companyName):
        if not self.hasCompany(companyName):
            print("This company is not in our Data Base, please try again!")
            return list()
        
        listOfEmployees = list()
        companyID = self.getCompanyID(companyName)
        for person in self.__peopleJson:
            if person["company_id"] == companyID:
                listOfEmployees.append(person["name"])
        if len(listOfEmployees) == 0:
            return list(["This company has no employees registered in our database."])
        return listOfEmployees
    
    def getPersonalInformation(self, person):
        if not self.hasPerson(person):
            print("This person is not in our Data Base, please try again!")
            return dict()
        
        infoDict = dict()
        personID = self.getPersonID(person)
        for attribute in self.__peopleJson[personID]:
            infoDict[attribute] = self.__peopleJson[personID][attribute]
            
#        Split the favouriteFood list in fruits and vegetables
        infoDict["fruits"] = [fruit for fruit in infoDict["favouriteFood"] if fruit == "banana" or \
                 fruit == "apple" or fruit == "orange" or fruit == "strawberry"]
        infoDict["vegetables"] = [vegetable for vegetable in infoDict["favouriteFood"] if vegetable == "beetroot" or \
                 vegetable == "carrot" or vegetable == "cucumber" or vegetable == "celery"]
        return infoDict
    
    def getCommonFriends(self, personA, personB):
        if not self.hasPerson(personA):
            print(personA + " is not in our Data Base, please try again!")
            return list()
        if not self.hasPerson(personB):
            print(personB + " is not in our Data Base, please try again!")
            return list()
        
        commonFriends = list()
        friendsPersonA = self.getPersonalInformation(personA)["friends"]
        friendsPersonB = self.getPersonalInformation(personB)["friends"]
        
        for friendOfA in friendsPersonA: 
            friendOfAInfo = self.getPersonalInformation(self.__peopleJson[friendOfA["index"]]["name"]);
            commonFriends += [self.__peopleJson[friendOfA["index"]]["name"] for friendOfB in friendsPersonB \
                              if friendOfA["index"] == friendOfB["index"] and \
                              friendOfAInfo["eyeColor"] == "brown" and \
                              friendOfAInfo["has_died"] == False]
        return commonFriends
    
    def parseInput(self, inputData):
        return [x.strip() for x in inputData.split(',') if x != '']
    
#    Returns a boolean mask of the itens in argList which are companies
    def checkInputForCompanies(self, argList):
        inputCompaniesCheckList = list()
        for element in argList:
            inputCompaniesCheckList.append(self.hasCompany(element))
        return inputCompaniesCheckList
  
#    Returns a boolean mask of the itens in argList which are people
    def checkInputForPeople(self, argList):
        inputPeopleCheckList = list()
        for element in argList:
            inputPeopleCheckList.append(self.hasPerson(element))
        return inputPeopleCheckList
    
    def getCompaniesOutput(self, companies):
        returnStr = ""
        for company in companies:
            returnStr += ''.join(["Employees at ", company, ":\n\t"])
            returnStr += '\n\t'.join(self.getEmployeesList(company))
            returnStr += '\n'
        return returnStr

    def getTwoPeopleOutput(self, peopleNames):
        if len(peopleNames) != 2:
            return "Please, enter two names"
        returnStr = ""
        for person in peopleNames:
            personalInfo = self.getPersonalInformation(person)
            returnStr += ''.join(["Information about ", person, ":"])
            returnStr += '\n\tAge: ' + str(personalInfo["age"])
            returnStr += '\n\tAddress: ' + personalInfo["address"]
            returnStr += '\n\tPhone: ' + personalInfo["phone"]
            returnStr += '\n'
        returnStr += "\nTheir common, alive and brown eyed, friend(s) is/are: " + ', '.join(self.getCommonFriends(peopleNames[0], peopleNames[1]))
        return returnStr
    
    def getOnePersonOutput(self, personName):
        personalInfo = self.getPersonalInformation(personName)
        returnStr = str(json.dumps({"username": personalInfo["email"], "age": str(personalInfo["age"]), \
                          "fruits": personalInfo["fruits"], "vegetables": personalInfo["vegetables"]}, sort_keys = False))
        return returnStr
        
    def validateInput(self, argList):
        argList = self.parseInput(argList)
        inputCompaniesCheckList = self.checkInputForCompanies(argList)
        inputPeopleCheckList = self.checkInputForPeople(argList)
        inputCompaniesCount = inputCompaniesCheckList.count(True)
        inputPeopleCount = inputPeopleCheckList.count(True)
        
#        if any received argument wasn't found in our data base, abort and asks for misspelling check
#        Otherwise, applyes the challenge rules for each expected situation
        if len(argList) != inputCompaniesCount + inputPeopleCount:
            notFound = ', '.join(arg for i, arg in enumerate(argList) if (not inputCompaniesCheckList[i] and not inputPeopleCheckList[i]))
            return "Warning: \"" + notFound + "\" was not found in our Data Base! Aborting Search...\nPlease, check for misspelling and try again!"
        elif inputCompaniesCount > 0 and inputPeopleCount == 0:
            return self.getCompaniesOutput(argList)
        elif inputCompaniesCount == 0 and inputPeopleCount == 2:
            return self.getTwoPeopleOutput(argList)
        elif inputCompaniesCount == 0 and inputPeopleCount == 1:
            return self.getOnePersonOutput(argList[0])
        else:
            return "No matches...\nPlease, type only company name(s) OR 1 or 2 people names per search"

    def __init__(self, companiesDir, peopleDir):
        self.loadCompaniesDB(companiesDir);
        self.loadPeopleDB(peopleDir);
        self.mapNames();