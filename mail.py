import win32com.client

def send_mail(text:str, subject:str, recipient:list, copyRecipient:list=[], 
 blindRecipient:list=[], attachment:list=[]):
    o = win32com.client.Dispatch("Outlook.Application")

    Msg = o.CreateItem(0)
    Msg.To = '; '.join(recipient)

    if copyRecipient != []:
        Msg.CC = '; '.join(copyRecipient)
    if blindRecipient != []:
        Msg.BCC = '; '.join(blindRecipient)

    Msg.Subject = subject
    Msg.Body = text

    for x in attachment:
        Msg.Attachments.Add(x)

    Msg.Send()
