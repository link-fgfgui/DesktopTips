from FLBasicModule import LSS



app = LSS.QtCore.QCoreApplication([])
lss = LSS.LocalSocSer("close", None)
send="exit" #exit/ST20:24:58/ST20:34:58
send=send.encode()
lss.send_message("DesktopTips", bytes(send))
app.exit()
