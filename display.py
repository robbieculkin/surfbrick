from get_data import data
import time
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode (IO.BCM)

# PINS
DATA_SWELL_H = 25
DATA_SWELL_P = 22
DATA_WIND_K  = 23
DATA_WIND_G  = 24
CLOCK = 17
SHIFT = 18

while(1):
    #get info from get_data.py
    data = data()

    #choose what goes in each digit: 0-ones place, 1-tens place
    swell_h0 = int(round(data['swell']['h']%10))
    swell_h1 = int(data['swell']['h']/10)
    swell_p0 = int(round(data['swell']['p']%10))
    swell_p1 = int(data['swell']['p']/10)

    wind_k0 = int(round(data['wind']['kts']%10))
    wind_k1 = int(data['wind']['kts']/10)
    wind_g0 = int(round(data['wind']['gust']%10))
    wind_g1 = int(data['wind']['gust']/10)

    #translate each digit to array of length 8 (segs + decimal pt) for YSD-160AR4B-8
    to7seg = {
        0:[1,0,0,0,1,0,0,0],
        1:[1,1,1,0,1,0,1,1],
        2:[0,1,0,0,1,1,0,0],
        3:[0,1,0,0,1,0,0,1],
        4:[0,0,1,0,1,0,1,1],
        5:[0,0,0,1,1,0,0,1],
        6:[0,0,0,1,1,0,0,0],
        7:[1,1,0,0,1,0,1,1],
        8:[0,0,0,0,1,0,0,0],
        9:[0,0,0,0,1,0,1,1]}

    #pair digits back up for sr
    swell_h = to7seg[swell_h0] + to7seg[swell_h1]
    swell_p = to7seg[swell_p0] + to7seg[swell_p1]
    wind_k =  to7seg[wind_k0]  + to7seg[wind_k1]
    wind_g =  to7seg[wind_g0]  + to7seg[wind_g1]

    #load shift registers with appropriate digits
    for ii in range(16): #16 because 16 segments in pair of digits
        # pull data pin
        IO.output(DATA_SWELL_H, swell_h[ii])
        IO.output(DATA_SWELL_P, swell_p[ii])
        IO.output(DATA_WIND_K,  wind_k[ii])
        IO.output(DATA_WIND_G,  wind_g[ii])
        time.sleep(0.1)
        # rising edge to load sr
        IO.output(CLOCK, 1)
        time.sleep(0.1)
        IO.output(CLOCK, 0)
        time.sleep(0.1)

    #pulse to display
    IO.output(SHIFT, 1)
    time.sleep(0.1)
    IO.output(SHIFT, 0)

    # TODO direction on compass - neopixels

    #sleep for 30 mins before updating - weather underground free API restriction
    time.sleep(60*30)
