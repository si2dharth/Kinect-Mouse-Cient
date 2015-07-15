import socket, sys
import win32api, win32con, math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.137.37', 8000)
sock.connect(server_address)
sock.send(b"HandRight|Width|1920|Height|1080|HandLeft|Output|2|LeftState|RightState")
x = 0
y = 0


def moveTo(x,y):
    #win32api.SetCursorPos((x,y)) 
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0,0)

def mouseDown(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

def mouseUp(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def scroll(x,y,amount):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x,y,amount,0)
    print(amount)

def uncompressNumber(s):
    #return (ord(s[0])-128)*255 + (ord(s[1])-128)
    return (ord(s[0])*255 + ord(s[1]))

def uncompressVector(s):
    return (uncompressNumber(s[0:2]),uncompressNumber(s[2:4]))

lastPosition = (0,0)
newPosition = (0,0)
lastY = 0
newY = 0
changeY = 0
newClick = False
click = False
newScroll = False
#scroll = False

def unpack(s):
    global newPosition
    global newClick
    global newY
    global newScroll
    res = {}
    while (s != ""):
        if (s[0] == '9' or s[0] == '8'):
            newPosition = uncompressVector(s[1:5])
            newClick = (s[0] == '9')
            s = s[5:]
        elif (s[0] == '5' or s[0] == '4'):
            newY = uncompressVector(s[1:5])[1]
            newScroll = (s[0] == '5')
            s = s[5:]
    return res

lastPosition = (0,0)
"""
while(True):
    data = b""
    c = None
    while c != b'\n':
        c = sock.recv(1)
        if c!=b'\n' : data += c
    data = data.decode('ISO-8859-1')
    data = unpack(data)
    #print(data)
    #print(newPosition)
    moveTo(newPosition[0] - lastPosition[0], newPosition[1] - lastPosition[1])
    if (newClick != click):
        if (newClick):
            mouseDown(0,0)
            print("CLick")
        else:
            mouseUp(0,0)
            print("No Click")
        click = newClick
    lastPosition = newPosition
    
    if (newScroll or changeY != 0):
        if (newScroll):
            scroll(0, 0, newY - lastY)
            changeY = newY - lastY
        else:
            scroll(0, 0, changeY)
            if (changeY > 0): changeY -= 1
            else: changeY += 1

    lastY = newY
    if ('MousePosition' in data):
        x = int(data['MousePosition'][0])
        y = int(data['MousePosition'][1])
        moveTo(x,y)

    if ('MouseClick' in data):
        mouseDown(x,y)
        mouseUp(x,y)
    else: 
        if ('MouseDrag' in data):
            if (data['MouseDrag']): mouseDown(x,y) 
            else: mouseUp(x,y)

    if ('Scroll' in data):
        scroll(x,y,data['Scroll'])
"""
def readPython():
    data = b"";
    nBracket = None
    while (nBracket != 0):
        c = sock.recv(1)
       # print(nBracket)
        if (c == b'{'):
            if (nBracket == None): nBracket = 1
            else: nBracket += 1
        if (c == b'}'): nBracket -= 1
        data += c

    data = data.decode('utf-8')
    data = eval(data)
    return data

def readStream():
    #HandRight, HandLeft, LeftState,RightState
    recv = b""
    for i in range(0,10):
        recv += sock.recv(1)
    
    recv = recv.decode('ISO-8859-1')

    data = {}
    data['HandRight'] = uncompressVector(recv[0:4])
    data['HandLeft'] = uncompressVector(recv[4:8])
    data['LeftState'] = (recv[8] == 'O')
    data['RightState'] = (recv[9] == 'O')
    return data

def readCompressedData():
    ""

while (True):
    print(readStream())

