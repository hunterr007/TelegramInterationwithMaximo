################################################################
# C_TELEGRAM - Object Launch Point - SR
# Revision: 1
#
# Developed by: Prashant Sharma
#   
# Purpose: Send Notification payload to Telegram
#
################################################################


from com.ibm.json.java import JSONArray, JSONObject
from psdi.mbo import  MboSet, MboConstants
from psdi.server import MXServer 
from java.nio.charset import StandardCharsets
from java.io import BufferedReader, InputStreamReader, OutputStream
from java.net import URL, HttpURLConnection , URLEncoder
from sys import *
from java.lang import *

#Set Login Information
mxServer = MXServer.getMXServer()
userInfo = mxServer.getUserInfo("maxadmin")

#Get Telegram API URL
PropSet = MXServer.getMXServer().getMboSet("maxpropvalue", userInfo)
PropSet.setWhere("PROPNAME = 'c_telegram.api.context.url'")
PropSet.reset()
if PropSet.isEmpty() == False:
	propMbo = PropSet.getMbo(0)
	tCxtURL = str(propMbo.getString("PROPVALUE"))
	
PropSet = MXServer.getMXServer().getMboSet("maxpropvalue", userInfo)
PropSet.setWhere("PROPNAME = 'c_telegram.bot.id'")
PropSet.reset()
if PropSet.isEmpty() == False:
	propMbo = PropSet.getMbo(0)
	tBotId = str(propMbo.getString("PROPVALUE"))
	
PropSet = MXServer.getMXServer().getMboSet("maxpropvalue", userInfo)
PropSet.setWhere("PROPNAME = 'c_telegram.chatid'")
PropSet.reset()
if PropSet.isEmpty() == False:
	propMbo = PropSet.getMbo(0)
	tChatId = str(propMbo.getString("PROPVALUE"))


srStatus = mbo.getString("STATUS")
srNum = mbo.getString("TICKETID")
srDesc = mbo.getString("DESCRIPTION")
assetNum = mbo.getString("ASSETNUM")

if srStatus == "NEW":
	notification = "Service Request :"+ srNum +" for Asset : "+ assetNum + " with Description: "+ srDesc +" has been created. Please Review."
	
	#Setting Parameters after encoding the values for Post Call     
	telegramURL=tCxtURL+tBotId+"/sendMessage"
	enCodeURL = StringBuilder(telegramURL)
	enCodeURL.append("?chat_id=")
	enCodeURL.append(URLEncoder.encode(tChatId, "UTF-8"))
	enCodeURL.append("&text=");
	enCodeURL.append(URLEncoder.encode(notification,"UTF-8"));
	
	url = URL(str(enCodeURL))
	con = url.openConnection()
	con.setRequestMethod('POST')
	con.setDoOutput(True)
	os = con.getOutputStream()
	responseCode = con.getResponseCode()
	os.flush()
	os.close()
	con.disconnect()
	
	if responseCode == 200:
		service.log("Response String:"+str(con.getResponseMessage()))