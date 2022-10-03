def stringTOlist(str:str, seperator:str='\n', limit:int=0):
    list = []
    # Parse string to list
    listRows = str.split(seperator)
    # If limit is set
    if limit != 0:
        for idx, x in enumerate(listRows):
            list.append(x)
            # If limit is reached
            if idx == limit:
                break
    # If limit isn't set
    else:
        list = str.split(seperator)
    # Return array (2D)
    return list

def listTOdict(list:list, seperator:str=';', removeQuotes:bool=False):
    dict = {}
    # Parse list to dictionary
    for strRow in list:
        if strRow != '':
            listRow = strRow.split(seperator)
            dict[listRow[0]] = listRow[1]
    return dict

def listTOdictModules(list:list, seperator:str=';', removeQuotes:bool=True, containsHeaders:bool=True):
    dict = {}
    # Get header
    listHeader = list[0].split(seperator)
    listName = list[1].split(seperator)
    for i in range(2, len(listHeader)):
        dict[listHeader[i]] = {'Name':listName[i], 'Modules':{}}
    # Parse list to dictionary
    for i in range(2, len(list)):
        listRow = list[i].split(seperator)
        if listRow != ['']:
            for j in range(2, len(listRow)):
                if int(listRow[j]) == 1:
                    dict[listHeader[j]]['Modules'][listRow[0]] = listRow[1]
    return dict

def listTOdictOptionals(list:list, seperator:str=';', removeQuotes:bool=True, containsHeaders:bool=True):
    dict = {}
    # Get header
    listHeader = list[0].split(seperator)
    listName = list[1].split(seperator)
    for i in range(2, len(listHeader)):
        dict[listHeader[i]] = {'Name':listName[i], 'Step':{}}
    # Parse list to dictionary
    for i in range(2, len(list)):
        listRow = list[i].split(seperator)
        if listRow != ['']:
            for j in range(2, len(listRow)):
                if listRow[j] != '':
                    if int(listRow[j]) == 1:
                        dict[listHeader[j]]['Step'][listRow[0]] = listRow[1]
    return dict
