from pprint import pprint as pp
import os
import time

from settings import Settings
from fileHandling import getLatestFileFromSubfolder, getTimeStamp, getLatestFile, readTXT, readTXTlines
from parseFunctions import stringTOlist, listTOdictModules, listTOdictOptionals
from jsonFunctions import writeJSON
from mail import send_mail

rootFile = __file__
rootFolder = rootFile.rsplit('\\', 1)[0] + '\\'

oSettings = Settings()

def getFile(directory:str, folderName:str='', fileName:str='', fileExtention:str=''):
    file = None
    file = getLatestFileFromSubfolder(directory, folderName, fileName, fileExtention)
    for i in range(int(oSettings.orderRetryAmount)):
        if file != None:
            return file
        file = getLatestFileFromSubfolder(directory, folderName, fileName, fileExtention)
        print(getTimeStamp() + ' - File ' + fileName + fileExtention + ' in folder ' + folderName + ' not found!')
        time.sleep(int(oSettings.orderRetryInterval))

def createOrderData(folderDestination:str):
    seperator = ';'
    strFolder = getTimeStamp().split('_')[0]
    fileOrders = getFile(oSettings.orderFolder, strFolder, oSettings.orderFile, oSettings.orderExt)
    if fileOrders == None:
        strMail = 'File ' + oSettings.orderFile + oSettings.orderExt + ' in folder ' + strFolder + ' not found!'
        print(strMail)
        send_mail(strMail, 'KSK Orders not found [NO_REPLY]', oSettings.mailRecipients)
        return False
    listData = readTXTlines(fileOrders.path)
    # Get header data
    dictHeader = {}
    listHeaders = listData[0].split(seperator)
    for j in range(len(listHeaders)):
        dictHeader[listHeaders[j].replace('="', '').replace('"', '')] = j
    # Get data
    dictOrder = {}
    for i in range(1, len(listData)):
        listRow = listData[i].split(seperator)
        if listRow != ['']:
            for i in range(len(listRow)):
                listRow[i] = listRow[i].replace('="', '').replace('"', '')
            strSO = listRow[dictHeader[oSettings.orderSOnr]]
            if strSO not in dictOrder:
                dictOrder[strSO] = {
                    'OrderStatus': listRow[dictHeader[oSettings.orderStatus]],
                    'Project': listRow[dictHeader[oSettings.orderProject]],
                    'Phase': listRow[dictHeader[oSettings.orderPhase]],
                    'WoPa': listRow[dictHeader[oSettings.orderWoPa]],
                    'Typ': listRow[dictHeader[oSettings.orderTyp]],
                    'SX': listRow[dictHeader[oSettings.orderSX]],
                    'EU': listRow[dictHeader[oSettings.orderEU]],
                    'Step':{}, 'AddWH':{}, 'OptionalWH':{}, 'BOM':[], 'Containing':{}, 'NotKSK':{}
                }
            if listRow[dictHeader[oSettings.orderKOGR]] == oSettings.orderKOGRvalue:
                dictOrder[strSO]['BOM'].append(listRow[dictHeader[oSettings.orderSNR]][0:7])
    writeJSON(folderDestination + 'Orders.json', dictOrder)
    if os.path.exists(oSettings.outputFolder + oSettings.outputSubfolder):
        writeJSON(oSettings.outputFolder + oSettings.outputSubfolder + 'Orders_' + getTimeStamp() + '.json', dictOrder)
    print()
    print(fileOrders.path)
    print('\nAmount orders:          ', len(dictOrder))
    return True

def createNotKSK(folderDestination:str):
    # Settings
    fileName = 'NotKSK'
    fileExt = '.csv'
    # Get data
    strData = readTXT(oSettings.sourceFolder + fileName + fileExt)
    listData = stringTOlist(strData)
    # Set data
    dictData = {}
    for i in range(1, len(listData)):
        if listData[i] != '':
            listRow = listData[i].split(';')
            dictData[listRow[0]] = listRow[1]
    # Write data
    writeJSON(folderDestination + fileName + '.json', dictData)
    print(fileName, len(dictData))
    #pp(dictData)

def createModuleJSON(folderDestination:str):
    fileExt = '.csv'
    listFiles = ['F60_LL_V8', 'F60_RL_V8', 'F57_LL_V11', 'F57_RL_V11']
    for fileName in listFiles:
        strData = readTXT(oSettings.sourceFolder + fileName + fileExt)
        listData = stringTOlist(strData)
        dictData = listTOdictModules(listData)
        writeJSON(folderDestination + fileName + '.json', dictData)
        print(fileName, len(dictData))

def createOptionalMD(folderDestination:str):
    # Settings
    fileName = 'OptionalMD'
    fileExt = '.csv'
    # Get data
    strData = readTXT(oSettings.sourceFolder + fileName + fileExt)
    listData = stringTOlist(strData)
    # Set data
    dictData = listTOdictOptionals(listData)
    # Write data
    writeJSON(folderDestination + fileName + '.json', dictData)
    print(fileName, len(dictData))
