class Settings:
    def __init__(self):
        self.patternSNR = "^[0-9][A-Z0-9]{6}$"
        # Source
        self.sourceFolder = "###"
        self.sourceFileList = [
            "###",
            "###"
        ]
        self.sourceFileList_1122 = [
            "###",
            "###"
        ]
        self.sourceExt = ".csv"
        # Output
        self.outputFolder = "###"
        self.outputSubfolder = "JSON/"
        # Orders
        self.orderFolder = "###"
        self.orderFile = "LccOrderCheck"
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
            "###",
            "###"
        ]
        # Typ lists
        self.F60_ICE = [
            "###",
            "###",
            "###"
        ]
