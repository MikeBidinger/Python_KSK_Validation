from pprint import pprint as pp
import os
import re

from settings import Settings
from createData import createOrderData
from jsonFunctions import readJSON, writeJSON
from fileHandling import getTimeStamp, writeResultList, writeResultDict
from mail import send_mail

debug_1 = bool(0)
debug_2 = bool(0)

print('\n')

rootFile = __file__
rootFolder = rootFile.rsplit('\\', 1)[0] + '\\'

oSettings = Settings()

timeStamp = getTimeStamp()

def getModuleJSONs(folder:str, listFiles:list):
    dict = {}
    for fileName in listFiles:
        dictTmp = readJSON(folder + fileName + '.json')
        dict = {**dict, **dictTmp}
    return dict

# Get order data
if not debug_2:
    if createOrderData(rootFolder):
        dictOrders = readJSON(rootFolder + 'Orders.json')
    else:
        strMail = 'ERROR: Order data not created!'
        print(strMail)
        if not debug_1:
            send_mail(strMail, 'KSK Order not found [NO_REPLY]', oSettings.mailRecipients)
else:
    dictOrders = readJSON(rootFolder + 'Orders.json')
    print('\nAmount orders:          ', len(dictOrders))

# Get step-module data
dictModules = getModuleJSONs(rootFolder, oSettings.sourceFileList)
print('Amount WH KSK:          ', len(dictModules))

# Get step-module data 11/22
dictModules_1122 = getModuleJSONs(rootFolder, oSettings.sourceFileList_1122)
print('Amount WH KSK 11/22:    ', len(dictModules_1122))

# Get optional-module data
dictOptional = readJSON(rootFolder + 'OptionalMD.json')
print('Amount optional modules:', len(dictOptional))

# Get NotKSK data
dictNotKSK = readJSON(rootFolder + 'NotKSK.json')
print('Amount Not KSK:         ', len(dictNotKSK))

# Add step data to each serie order
removeOrder = []
for order, itemOrder in dictOrders.items():
    if itemOrder['WoPa'] >= '20220727' and (itemOrder['Phase'] == 'KBB' or itemOrder['Project'] == '' or (itemOrder['Project'] == 'Y22' and itemOrder['Phase'] == 'SVL')):
        if itemOrder['WoPa'] < '20221144':
            removeSNR = []
            for snr in itemOrder['BOM']:
                if snr in dictModules:
                    if itemOrder['Step'] == {}:
                        itemOrder['Step'] = {**{'SNR':snr},**dictModules[snr]}
                        removeSNR.append(snr)
                    else:
                        # Multiple steps found
                        itemOrder['Step']['SNR'] = 'Multiple Steps (' + itemOrder['Step']['SNR'] + '-' + snr + ')'
                        removeSNR.append(snr)
            # No step found
            if itemOrder['Step'] == {}:
                itemOrder['Step']['SNR'] = 'Missing Step'
            # Remove found step
            else:
                for x in removeSNR:
                    itemOrder['BOM'].remove(x)
        elif itemOrder['Typ'] not in oSettings.F60_ICE:
            removeSNR = []
            for snr in itemOrder['BOM']:
                if snr in dictModules_1122:
                    if itemOrder['Step'] == {}:
                        itemOrder['Step'] = {**{'SNR':snr},**dictModules_1122[snr]}
                        removeSNR.append(snr)
                    else:
                        # Multiple steps found
                        itemOrder['Step']['SNR'] = 'Multiple Steps (' + itemOrder['Step']['SNR'] + '-' + snr + ')'
                        removeSNR.append(snr)
            # No step found
            if itemOrder['Step'] == {}:
                itemOrder['Step']['SNR'] = 'Missing Step'
            # Remove found step
            else:
                for x in removeSNR:
                    itemOrder['BOM'].remove(x)
        else:
            itemOrder['Step']['SNR'] = 'JIS'
    else:
        removeOrder.append(order)

# Remove non-serie orders
for order in removeOrder:
    dictOrders.pop(order)

# Check each order
for order, itemOrder in dictOrders.items():
    # If order contains only one step
    if re.search(oSettings.patternSNR, itemOrder['Step']['SNR']) != None:
        removeSNR = []
        # For each snr in order:
        for snr in itemOrder['BOM']:
            if snr in itemOrder['Step']['Modules']:
                itemOrder['Containing'][snr] = itemOrder['Step']['Modules'][snr]
                removeSNR.append(snr)
            elif snr in dictNotKSK:
                itemOrder['NotKSK'][snr] = dictNotKSK[snr]
                removeSNR.append(snr)
        # Remove snr's found in order
        for snr in removeSNR:
            itemOrder['BOM'].remove(snr)
        # For each module in step
        for module in itemOrder['Step']['Modules']:
            if module not in itemOrder['Containing']:
                if module not in dictOptional:
                    itemOrder['AddWH'][module] = itemOrder['Step']['Modules'][module]
                else:
                    itemOrder['OptionalWH'][module] = itemOrder['Step']['Modules'][module]
    else:
        for snr in itemOrder['BOM']:
            if snr in dictModules:
                itemOrder['Step']['Unjustified'] = snr

writeJSON(rootFolder + 'Result.json', dictOrders)
if not debug_2:
    if os.path.exists(oSettings.outputFolder + oSettings.outputSubfolder):
        writeJSON(oSettings.outputFolder + oSettings.outputSubfolder + 'Result_' + getTimeStamp() + '.json', dictOrders)

# Create report data
listOrderOK = []
listOrderCheck = []
listStepMissing = []
listStepMulti = []
listStepAddition = []
dictStepAddition = {'Module;Step_SNR;Step_Description;ModelCode':'Order(s)'}
listBOMaddition = []
dictBOMaddition = {'Module;Step_SNR;Step_Description;ModelCode':'Order(s)'}
listUnjustifiedStep = []
for order, itemOrder in dictOrders.items():
    if re.search(oSettings.patternSNR, itemOrder['Step']['SNR']) != None:
        if len(itemOrder['AddWH']) == 0 and len(itemOrder['BOM']) == 0:
            if itemOrder['EU'] == 'UN108B':
                listOrderOK.append(order)
        else:
            listOrderCheck.append(order)
            if len(itemOrder['AddWH']) > 0:
                if itemOrder['EU'] != 'UN108B':
                    listStepAddition.append(order)
                    for x in itemOrder['AddWH']:
                        strKey =  ';'.join([x, itemOrder['Step']['SNR'], itemOrder['Step']['Name'], itemOrder['Typ']])
                        if strKey in dictStepAddition:
                            dictStepAddition[strKey] = dictStepAddition[strKey] + ' / ' + order
                        else:
                            dictStepAddition[strKey] = order
            if len(itemOrder['BOM']) > 0:
                if itemOrder['EU'] != 'UN108B':
                    listBOMaddition.append(order)
                    for x in itemOrder['BOM']:
                        strKey =  ';'.join([x, itemOrder['Step']['SNR'], itemOrder['Step']['Name'], itemOrder['Typ']])
                        if strKey in dictBOMaddition:
                            dictBOMaddition[strKey] = dictBOMaddition[strKey] + ' / ' + order
                        else:
                            dictBOMaddition[strKey] = order
    elif itemOrder['Step']['SNR'] == 'Missing Step':
        listOrderCheck.append(order)
        if itemOrder['EU'] != 'UN108B':
            listStepMissing.append(order)
    elif 'Multiple Steps' in itemOrder['Step']['SNR']:
        listOrderCheck.append(order)
        if itemOrder['EU'] != 'UN108B':
            listStepMulti.append(order)
    elif 'Unjustified' in itemOrder['Step']:
        listOrderCheck.append(order)
        if itemOrder['EU'] != 'UN108B':
            listUnjustifiedStep.append(order)

listMail = []
listMail.append(str(len(dictOrders)) + " orders checked")
listMail.append(str(len(listOrderOK)) + " WH KSK orders correct with Package")
listMail.append(str(len(listStepMissing)) + " WH KSK orders missing Step harness")
listMail.append(str(len(listStepMulti)) + " WH KSK orders containing multiple Step harness")
listMail.append(str(len(listStepAddition)) + " WH KSK orders containing additional Step modules")
listMail.append(str(len(listBOMaddition)) + " WH KSK orders containing additional BOM modules")
listMail.append(str(len(listUnjustifiedStep)) + " JIS KSK orders containing Step harness")

print('\n')
print('\n'.join(listMail) + '\n')

print('\nFailed Orders:', len(listOrderCheck))
if not debug_1:
    filePath = writeResultList(listOrderCheck, oSettings.outputFolder + 'FailedOrders\\', 'Failed_Orders', timeStamp)
    print('Failed Orders result file written:\n', filePath)

listAttachment = []

if len(listOrderOK) > 0:
    print('\nOrders correct with Package:')
    pp(listOrderOK)
    if not debug_1:
        filePath = writeResultList(listOrderOK, oSettings.outputFolder, 'Order_OK', timeStamp)
        print('Orders correct with Package result file written:\n', filePath)
        listAttachment.append(filePath)

if len(listStepMissing) > 0:
    print('\nMissing Step harness:')
    pp(listStepMissing)
    if not debug_1:
        filePath = writeResultList(listStepMissing, oSettings.outputFolder, 'Missing_Step', timeStamp)
        print('Missing Step result file written:\n', filePath)
        listAttachment.append(filePath)

if len(listStepMulti) > 0:
    print('\nMulitple Step harness:')
    pp(listStepMulti)
    if not debug_1:
        filePath = writeResultList(listStepMulti, oSettings.outputFolder, 'Multiple_Step', timeStamp)
        print('Multiple Step result file written:\n', filePath)
        listAttachment.append(filePath)

if len(listStepAddition) > 0:
    print('\nAdditional Step modules:')
    pp(dictStepAddition)
    if not debug_1:
        filePath = writeResultList(listStepAddition, oSettings.outputFolder, 'Step_Addition', timeStamp)
        print('Step addition result file written:\n', filePath)
        listAttachment.append(filePath)

if len(listBOMaddition) > 0:
    print('\nAdditional BOM modules:')
    pp(dictBOMaddition)
    if not debug_1:
        filePath = writeResultList(listBOMaddition, oSettings.outputFolder, 'BOM_Addition', timeStamp)
        print('BOM addition result file written:\n', filePath)
        listAttachment.append(filePath)

if not debug_1:
    send_mail('\n'.join(listMail), 'KSK Check results [NO_REPLY]', oSettings.mailRecipients, attachment=listAttachment)

if not debug_1:
    if len(listStepAddition) > 0:
        writeResultDict(dictStepAddition, oSettings.outputFolder, 'Step_Addition_Detail', timeStamp)
    if len(listBOMaddition) > 0:
        writeResultDict(dictBOMaddition, oSettings.outputFolder, 'BOM_Addition_Detail', timeStamp)
