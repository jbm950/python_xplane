#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      James
#
# Created:     09/03/2015
# Copyright:   (c) James 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
##import python_xplane_interface as pxi
import time,struct

# Following format of http://nbviewer.ipython.org/gist/kickapoo/2cec262723390d6f386a

def throttle_command(speed_read):

    # Universe of discourse
    speed = np.arange(60,150,.1)
    throttle_value = np.arange(0,1,0.01)

    # Input membership functions
    too_slow = fuzz.trapmf(speed,[60,60,80,85])
    slow = fuzz.trimf(speed,[83,90,97])
    cruise = fuzz.trimf(speed,[95,100,105])
    fast = fuzz.trimf(speed,[103,110,117])
    too_fast = fuzz.trapmf(speed,[115,120,150,150])

    # Output membership functions
    very_low = fuzz.trimf(throttle_value,[0,0,0.15])
    low = fuzz.trimf(throttle_value,[0.1,0.25,0.4])
    medium = fuzz.trimf(throttle_value,[0.35,0.5,0.65])
    high = fuzz.trimf(throttle_value,[0.6,0.75,0.9])
    very_high = fuzz.trimf(throttle_value,[0.85,1,1])

    # membership values
    speed_cat_too_slow = fuzz.interp_membership(speed,too_slow,speed_read)
    speed_cat_slow = fuzz.interp_membership(speed,slow,speed_read)
    speed_cat_cruise = fuzz.interp_membership(speed,cruise,speed_read)
    speed_cat_fast = fuzz.interp_membership(speed,fast,speed_read)
    speed_cat_too_fast = fuzz.interp_membership(speed,too_fast,speed_read)

    # If part of rules
    rule1 = speed_cat_too_slow
    rule2 = speed_cat_slow
    rule3 = speed_cat_cruise
    rule4 = speed_cat_fast
    rule5 = speed_cat_too_fast

    # Then part of rules
    imp1 = np.fmin(rule1,very_high)
    imp2 = np.fmin(rule2,high)
    imp3 = np.fmin(rule3,medium)
    imp4 = np.fmin(rule4,low)
    imp5 = np.fmin(rule5,very_low)

    aggregate_membership = np.fmax(imp1,np.fmax(imp2,np.fmax(imp3,np.fmax(imp4,imp5))))

    return fuzz.defuzz(throttle_value,aggregate_membership,'centroid')

# Self Test locally
speeds = np.arange(60,150,0.1)
y = np.zeros_like(speeds)
for i in range(len(speeds)):
    y[i] = throttle_command(speeds[i])

# Input membership functions
too_slow = fuzz.trapmf(speeds,[60,60,80,85])
slow = fuzz.trimf(speeds,[83,90,97])
cruise = fuzz.trimf(speeds,[95,100,105])
fast = fuzz.trimf(speeds,[103,110,117])
too_fast = fuzz.trapmf(speeds,[115,120,150,150])


plt.plot(speeds,y,speeds,too_slow,speeds,slow,speeds,cruise,speeds,fast,speeds,too_fast)
plt.xlabel('Airspeed (KIAS)')
plt.ylabel('Throttle Command/Speed Membership Functions')
plt.title('Throttle Commands vs. Airspeeds')
plt.legend(('Throttle Commands','Too Slow','Slow','Cruise','Fast','Too Fast'),bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0.)
plt.show()


### Test with x-plane
### Need to make sure that the ip address and send/recieve ports match your setup
##xp_inter = pxi.Xplane_connection('xplane ip address',49000,49001)
##
##try:
##    runtime = 30
##    start = time.time()
##
##    speeds = []
##    commands = []
##    timeofsim = []
##
##    while start + runtime > time.time():
##       speed = xp_inter.recieve()[1]
##       speeds.append(speed)
##       throt_command = throttle_command(speed)
##       commands.append(throt_command)
##       message = struct.pack('ifxxxxxxxxxxxxxxxxxxxxxxxxxxxx',25,throt_command)
##       xp_inter.send(message)
##       timeofsim.append(time.time() - start)
##
##    plt.subplot(2,1,1)
##    plt.plot(timeofsim,speeds)
##    plt.title('Speeds over time')
##    plt.ylabel('Speed')
##
##    plt.subplot(2,1,2)
##    plt.plot(timeofsim,commands)
##    plt.title('Throttle Commands over time')
##    plt.ylabel('Throttle Command')
##    plt.xlabel('Time of Simulation (s)')
##
##    plt.show()
##
##finally:
##    xp_inter.close()





