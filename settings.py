class Settings:
    def __init__(self):
        self.patternSNR = "^[0-9][A-Z0-9]{6}$"
        # Source
        self.sourceFolder = "//nedcar.nl/Office/Supply/3 LCC/015 IPT FAS/000 KSK variant reduction/100 Check Source Data/"
        self.sourceFileList = [
            "F60_LL_V4_1",
            "F60_RL_V4_1",
            "F57_LL_V4",
            "F57_RL_V4",
            "F60_LL_V5_1",
            "F60_RL_V5_1",
            "F57_LL_V8_2",
            "F57_RL_V8_2"
        ]
        self.sourceFileList_1122 = [
            "F60_LL_V8",
            "F60_RL_V8",
            "F57_LL_V11_2",
            "F57_RL_V11_2"
        ]
        self.sourceExt = ".csv"
        # Output
        self.outputFolder = "//nedcar.nl/office/Supply/3 PD_S/KBB 722 Opvolging/CheckResults/"
        self.outputSubfolder = "JSON/"
        # Orders
        self.orderFolder = "\\\\nedcar.nl\\ApolloP\\Shared_Data\\configuration_control\\BOD_Exports\\"
        self.orderFile = "LccOrderCheck"
        #self.orderFilePearl = "LccPearlOrderCheck"
        self.orderExt = ".csv"
        self.orderRetryInterval = "60" # in seconds
        self.orderRetryAmount = "180" # (3h * 60s)
        self.orderSOnr = "SALES_ORDER_NUMBER"
        self.orderStatus = "ORDER_STATUS_CODE"
        self.orderProject = "PROJECT"
        self.orderPhase = "PHASE"
        self.orderWoPa = "WOPAWOCH"
        self.orderTyp = "TYP"
        self.orderSNR = "PART_NUMBER"
        self.orderKOGR = "UPG_NUMBER"
        self.orderKOGRvalue = "6111"
        self.orderSX = "OP_049"
        self.orderEU = "UN108B"
        # Mail
        self.mailRecipients = [
            "m.bidinger@vdlnedcar.nl",
            "l.van.der.zon@vdlnedcar.nl",
            "e.weekers@vdlnedcar.nl",
            "m.hellenbrand@vdlnedcar.nl",
            "r.koks@vdlnedcar.nl",
            "f.dirx@vdlnedcar.nl",
            "m.geerling@vdlnedcar.nl",
            "mark.hermans@vdlnedcar.nl",
            "c.smeets@vdlnedcar.nl"
        ]
        # Typ lists
        self.F60_ICE = [
            "11BR",
            "11BS",
            "12BR",
            "21BR",
            "21BT",
            "21BU",
            "22BR",
            "22BT",
            "22BU",
            "23BR",
            "31BR",
            "31BS",
            "32BS",
            "33BS",
            "41BR",
            "41BT",
            "42BR",
            "42BT",
            "43BR",
            "51BR",
            "52BR",
            "53BR",
            "61BT",
            "62BT",
            "81BR",
            "81BT",
            "82BR",
            "82BT",
            "83BR"
        ]
