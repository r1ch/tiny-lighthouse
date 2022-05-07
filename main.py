import picounicorn
import utime
import math
import machine
 
picounicorn.init()

class Time:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute
        
    def datetime(self,hour=None,minute=None):
        self.hour = hour if hour is not None else self.hour
        self.minute = minute if minute is not None else self.minute
        
        return (self.hour, self.minute)
    
    def linear(self):
        return self.hour*60 + self.minute

class WrappedRTC:
    def __init__(self):
        self.rtc = machine.RTC()
        [year, month, day, weekday, hour, minute, seconds, subseconds] = self.rtc.datetime()
        self.rtc.datetime((year, month, day, weekday, 16, minute, seconds, subseconds))
        
    def datetime(self, hour=None, minute=None):
        [year, month, day, weekday, h, m, seconds, subseconds] = self.rtc.datetime()
        
        if (hour is not None) and (minute is not None):
            self.rtc.datetime((year, month, day, weekday, hour, minute, seconds, subseconds))
            [year, month, day, weekday, h, m, seconds, subseconds] = self.rtc.datetime()
        
        return (h,m)
    
    def linear(self):
        [hour,minute] = self.datetime()
        return hour*60 + minute
    
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
                [0,1,0],
                [1,0,1],
                [1,0,1],
                [1,0,1],
                [1,0,1],
                [1,0,1],
                [0,1,0],
            ],[
                [0,1,0],
                [1,1,0],
                [0,1,0],
                [0,1,0],
                [0,1,0],
                [0,1,0],
                [1,1,1],
            ],[
                [0,1,0],
                [1,0,1],
                [0,0,1],
                [0,1,0],
                [1,0,0],
                [1,0,0],
                [1,1,1],
            ],[
                [1,1,0],
                [0,0,1],
                [0,0,1],
                [1,1,0],
                [0,0,1],
                [0,0,1],
                [1,1,0],
            ],[
                [0,0,1],
                [0,1,1],
                [1,0,1],
                [1,1,1],
                [0,0,1],
                [0,0,1],
                [0,0,1],
            ],[
                [1,1,1],
                [1,0,0],
                [1,0,0],
                [1,1,0],
                [0,0,1],
                [0,0,1],
                [1,1,0],
            ],[
                [0,1,1],
                [1,0,0],
                [1,0,0],
                [1,1,0],
                [1,0,1],
                [1,0,1],
                [0,1,0],
            ],[
                [1,1,1],
                [0,0,1],
                [0,0,1],
                [0,1,0],
                [1,0,0],
                [1,0,0],
                [1,0,0],
            ],[
                [1,1,1],
                [1,0,1],
                [1,0,1],
                [0,1,0],
                [1,0,1],
                [1,0,1],
                [1,1,1],
            ],[
                [0,1,0],
                [1,0,1],
                [1,0,1],
                [0,1,1],
                [0,0,1],
                [0,0,1],
                [1,1,0],
            ]
        ]

# 0 = current, 1 = go green, 2 = go red, 3 = lighthouse
mode = 0
sleep = 0.5

greenTime = Time(7,0)
green = [0,255,0]

redTime = Time(19,0)
red = [245,40,20]

rtcTime = WrappedRTC()
white = [255,255,255]


while True:
    pressed = 0
    times = [rtcTime,greenTime,redTime]
    displays = [white,green,red]
    
    if picounicorn.is_pressed(picounicorn.BUTTON_A):
        pressed = 1
        mode = (mode + 1) % 4
    
    if picounicorn.is_pressed(picounicorn.BUTTON_B):
        pressed = 1
        mode = (mode - 1) % 4
        

    if mode <= 2:
        (hour,minute) = times[mode].datetime()
        if picounicorn.is_pressed(picounicorn.BUTTON_X):
            pressed = 2
            hour = (hour + 1) % 24 if minute == 59 else hour
            minute = (minute + 1) % 60
            times[mode].datetime(hour,minute)
        if picounicorn.is_pressed(picounicorn.BUTTON_Y):
            pressed = 2
            hour = (hour - 1) % 24 if minute == 0 else hour
            minute = (minute - 1) % 60
            times[mode].datetime(hour,minute)
         
        string = [n[math.floor(hour/10)],s,n[hour%10],s,s,n[math.floor(minute/10)],s,n[minute%10]]
          
        xOff = 0
        for item in string:
            for rowIdx, row in enumerate(item):
                for entryIdx, entry in enumerate(row):
                    picounicorn.set_pixel(entryIdx+xOff,rowIdx,displays[mode][0]*entry,displays[mode][1]*entry,displays[mode][2]*entry)
            xOff += len(item[0])
    
    if mode == 3:
        linearNow = rtcTime.linear()
        pixel = red
        if(linearNow < greenTime.linear() or linearNow >= redTime.linear()):
            pixel = red
        elif(linearNow - greenTime.linear() <= 60):
            pixel = green
        else:
            pixel = white
          
        for y in range(7):
            for x in range(16):
                picounicorn.set_pixel(x,y,pixel[0],pixel[1],pixel[2])
    
    if pressed>0:
        utime.sleep(sleep)
        if pressed == 2:
            sleep = sleep * 0.2
    else:
        sleep = 0.5
        
        
