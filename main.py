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
      
#a space in 7x1 leds (all off)    
s = [
            [0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]
        ]

#numbers : 0 to 9 in 7x3 leds  
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

#colours in rgb for the lighthouse
green = [0,255,0]
red = [245,40,20]
white = [255,255,255]

#as standard, turn green at 0700h
greenTime = Time(7,0)

#as standard, turn red at 1900h
redTime = Time(19,0)


rtcTime = WrappedRTC()


times = [rtcTime,greenTime,redTime]
displays = [white,green,red]

while True:
    pressed = 0

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
        # number for hour-tens, space, number for hours-ones, space, space, number for minute-tens, number for minute-ones
        string = [n[math.floor(hour/10)],s,n[hour%10],s,s,n[math.floor(minute/10)],s,n[minute%10]]
        
        # xOff is the x-Offset - how far right / which columns we are drawing
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
            #red light before wake (green) time, red light after sleep time
            pixel = red
        elif(linearNow - greenTime.linear() <= 60):
            #green light for an hour after wake (green) time
            pixel = green
        else:
            #don't confuse them; white if they are having a mid day nap
            pixel = white
        #every pixel  
        for y in range(7):
            for x in range(16):
                picounicorn.set_pixel(x,y,pixel[0],pixel[1],pixel[2])
    
    #presses make the response change faster (hold to skip many minutes)
    if pressed>0:
        utime.sleep(sleep)
        if pressed == 2:
            sleep = sleep * 0.2
    else:
        sleep = 0.5
