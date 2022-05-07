import picounicorn
import utime
import math
import machine

rtc = machine.RTC()

picounicorn.init()

s = [
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]
        ]

n = [
            [
                [0,0,0],
                [1,1,1],
                [1,0,1],
                [1,0,1],
                [1,0,1],
                [1,1,1],
                [0,0,0],
            ],[
                [0,0,0],
                [0,0,1],
                [0,1,1],
                [0,0,1],
                [0,0,1],
                [0,0,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [0,0,1],
                [1,1,1],
                [1,0,0],
                [1,1,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [0,0,1],
                [1,1,1],
                [0,0,1],
                [1,1,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,0,1],
                [1,0,1],
                [1,1,1],
                [0,0,1],
                [0,0,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [1,0,0],
                [1,1,1],
                [0,0,1],
                [1,1,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [1,0,0],
                [1,1,1],
                [1,0,1],
                [1,1,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [0,0,1],
                [0,1,0],
                [0,1,0],
                [0,1,0],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [1,0,1],
                [1,1,1],
                [1,0,1],
                [1,1,1],
                [0,0,0],
            ],[
                [0,0,0],
                [1,1,1],
                [1,0,1],
                [1,1,1],
                [0,0,1],
                [1,1,1],
                [0,0,0],
            ]
        ]

mode = 1
while True:
    [year, month, day, weekday, hours, minutes, seconds, subseconds] = rtc.datetime()
    
    string = [n[math.floor(hours/10)],s,n[hours%10],s,s,n[math.floor(minutes/10)],s,n[minutes%10]]

        
    if picounicorn.is_pressed(picounicorn.BUTTON_X):
        mode = 1
        print(minutes)
        rtc.datetime((year, month, day, weekday, (hours+1)%24 if minutes == 59 else hours, (minutes+1)%60, seconds, subseconds))

    if picounicorn.is_pressed(picounicorn.BUTTON_Y):
        mode = 1
        rtc.datetime((year, month, day, weekday, (hours-1)%24 if minutes == 0 else hours, (minutes-1)%60, seconds, subseconds))

    if picounicorn.is_pressed(picounicorn.BUTTON_A):
        mode = 0
        
    if mode == 1:    
        xOff = 0
        for item in string:
            for rowIdx, row in enumerate(item):
                for entryIdx, entry in enumerate(row):
                    picounicorn.set_pixel(entryIdx+xOff,rowIdx,255*entry,255*entry,255*entry)
            xOff += len(item[0])
    else:
        for y in range(7):
            for x in range(16):
                picounicorn.set_pixel(x,y,0,255,0)
                    
        
    
        