import os
from datetime import datetime

def getLatestFile(directory:str, filename:str='', fileExtention:str=''):
    creationTime = 0.0
    # Loop through directory
    for file in os.scandir(directory):
        # If object is a file
        if file.is_file():
            # If file extension matches
            if fileExtention in file.name or fileExtention == '':
                # If filename matches
                if filename in file.name or filename == '':
                    # Get creation datetime
                    if os.path.getctime(file.path) > creationTime:
                        creationTime = os.path.getctime(file.path)
                        latestFile = file
                    #print(datetime.utcfromtimestamp(creationTime), file.path)
    return latestFile

def getLatestFileFromSubfolder(directory:str, folderName:str, fileName:str='', fileExtention:str=''):
    creationTime = 0.0
    fileFound = False
    # Loop through directory
    for subfolder in os.scandir(directory):
        if subfolder.is_dir() and folderName in subfolder.name:
            for file in os.scandir(subfolder):
                # If object is a file
                if file.is_file():
                    # If file extension matches
                    if fileExtention in file.name or fileExtention == '':
                        # If filename matches
                        if fileName in file.name or fileName == '':
                            # Get creation datetime
                            fileFound = True
                            if os.path.getctime(file.path) > creationTime:
                                creationTime = os.path.getctime(file.path)
                                latestFile = file
                            #print(datetime.utcfromtimestamp(creationTime), file.path)
    if fileFound:
        return latestFile

def readTXT(filePath:str):
    strData = ''
    f = open(filePath, 'r')
    strData = f.read()
    f.close()
    return strData

def readTXTlines(filePath:str, nrLines:int=0, encoding:str=None):
    listData = []
    f = open(filePath, 'r', encoding=encoding)
    if nrLines == 0:
        listData = f.readlines()
        if listData[0][len(listData[0])-1:len(listData[0])] == '\n':
            for i in range(len(listData)):
                listData[i] = listData[i].rsplit('\n', 1)[0]
    else:
        for i in range(0, nrLines):
            listData.append(f.readline())
    f.close()
    return listData

def readCSVdict(filePath:str, key:str, headerLine:int=0, nrLines:int=0, encoding:str=None):
    # Read CSV file
    listData = readTXTlines(filePath, nrLines, encoding)
    # Parse CSV text to dict
    dictData = {}
    listHeader = listData[headerLine].split(';')
    for i in range(headerLine + 1, len(listData)):
        listRow = listData[i].split(';')
        dictVal = {}
        for idx, val in enumerate(listRow):
            dictVal[listHeader[idx]] = val
        dictData[dictVal[key]] = dictVal
    return dictData

def writeResultList(listResult:list, folderPath:str, fileName:str, timeStamp:str, fileExtension:str='.csv', bQoutes:bool=False):
    filePath = folderPath + fileName + "_" + timeStamp + fileExtension
    f = open(filePath, 'a')
    for valResult in listResult:
        if bQoutes:
            f.write('"' + valResult + '"' + '\n')
        else:
            f.write(valResult + '\n')
    f.close()
    return filePath

def writeResultDict(dictResult:dict, folderPath:str, fileName:str, timeStamp:str, fileExtension:str='.csv'):
    filePath = folderPath + fileName + "_" + timeStamp + fileExtension
    f = open(filePath, 'a')
    for key, val in dictResult.items():
        listKey = key.split(';')
        for x in listKey:
            f.write(x + ';')
        f.write(val + '\n')
    f.close()

def getTimeStamp():
    strDate = str(datetime.now()).replace('-', '').replace(':', '').replace('.', '').replace(' ', '_')
    return strDate
