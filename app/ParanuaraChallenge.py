import ParanuaraDB as PDB

def printHelp():
    print("\n==> How to search:" \
              "\n\tCompany name(s)    -> e.g: BEZAL, MEMORA" \
              "\n\tSingle Person      -> e.g: Bonnie Bass" \
              "\n\tTwo People         -> e.g: Carmella Lambert, Maribel Cruz" \
              "\n\tNote: For multi-search, separate itens using comma ','" \
              "\n\tType \"exit\" to shutdown or \"help\" to learn how to search")
    
db = PDB.ParanuaraDB('resources/companies.json', 'resources/people.json')
print ('-> Paranuara Challenge\n')
print ('Would you like to navigate through our data base?')
printHelp()

while True:
    inputData = input("\n===> What would you like to search?\n\t ")
    if inputData == "exit":
        break
    elif inputData == "help":
        printHelp()
    else:
        print("\n\nSearching...\n\nResults for \"" + inputData + "\":\n")
        print(db.validateInput(inputData))
print("\n\nBye!")