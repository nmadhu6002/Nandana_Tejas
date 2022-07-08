import math
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
from tkinter import *
import time

time_step = 0.001
real_time = 10 #s
total_time = int(real_time/time_step)
amplitude = 0.6 #rad
m = 1 #mass of ball (kg)
l = 1 #length of string (m)
g_const = 9.8 #gravitational constant
time_steps = [0]
for t in range(1, total_time):
    time_steps.append(time_steps[t-1] + time_step)

def Euler_Method():
    ang_pos = [amplitude] #angular position (rad)
    ang_vel = [-g_const*math.sin(amplitude)/l*time_step] #angular velocity
    for t in range(1, total_time):
        ang_pos.append(ang_pos[t-1] + ang_vel[t-1]*time_step)
        ang_vel.append(ang_vel[t-1] - g_const*math.sin(ang_pos[t-1])/l*time_step)
    return ang_pos, ang_vel

def Semi_Implicit(acceleration):
    ang_pos = [amplitude]  # angular position (rad)
    ang_vel = [acceleration(amplitude, 0, 0)*time_step]  # angular velocity
    for t in range(1, total_time):
        ang_vel.append(ang_vel[t-1] + acceleration(ang_pos[t-1], ang_vel[t-1], t-1)*time_step)
        ang_pos.append(ang_pos[t-1] + ang_vel[t]*time_step)
    return ang_pos, ang_vel

def Scipy():
    def equation_motion(u, x):
        return (u[1], -g_const*math.sin(u[0])/l)
    initial = [amplitude, 0]
    times = np.arange(0, real_time, time_step)
    ang_pos = odeint(equation_motion, initial, times)
    ang_pos = ang_pos[:,0]
    ang_vel = [0]
    for i in range(1, len(ang_pos)):
        ang_vel.append((ang_pos[i] - ang_pos[i-1])/time_step)
    return ang_pos, ang_vel
    

def acceleration(theta, ang_vel, t):
    if ang_vel == 0:
        return -g_const*math.sin(theta)/l
    elif ang_vel < 0:
        return -g_const*math.sin(theta)/l + 0.5
    else:
        return -g_const*math.sin(theta)/l - 0.5
# ang_pos = Scipy()[0]
# ang_vel = Scipy()[1]
ang_pos = Semi_Implicit(acceleration)[0]
ang_vel = Semi_Implicit(acceleration)[1]
# ang_pos = Euler_Method()[0]
# ang_vel = Euler_Method()[1]
kinetic_energy = [1/2*m*(_*l)**2 for _ in ang_vel]
potential_energy = [m*g_const*(l-l*math.cos(_)) for _ in ang_pos]
total_energy = [kinetic_energy[i] + potential_energy[i] for i in range(total_time)]
#print(ang_pos)
#-------------------#
#     ANIMATION
#-------------------#
#create canvas
tk = Tk()
canvas = Canvas(tk, width=400, height=400)
canvas.pack()

frame_step = int(0.001/time_step)
l_pix = l*150 #convert to length pixels
r = 20 #radius of ball
pos = [(200-l_pix*math.sin(ang_pos[i]), 200+l_pix*math.cos(ang_pos[i])) for i in range(len(ang_pos))] #cartesian position of ball
canvas.create_line(200, 200, pos[0][0], pos[0][1]) #create line
canvas.create_oval(pos[0][0]-r, pos[0][1]-r, pos[0][0]+r, pos[0][1]+r, fill='red') #create ball
for t in range(frame_step, total_time, frame_step):
    canvas.move(2, pos[t][0]-pos[t-frame_step][0], pos[t][1]-pos[t-frame_step][1]) #move ball
    canvas.coords(1, 200, 200, pos[t][0], pos[t][1]) #move 
    tk.update()

#-------------------#
#       PLOTS
#-------------------#
plt.figure(1)
plt.plot(time_steps, ang_pos)  # plotting angular position
plt.xlabel('time (s)')
plt.ylabel('angular displacement (rad)')

# plt.figure(2)
# plt.plot(time_steps, ang_vel)  # plotting angular velocity
# plt.xlabel('time (s)')
# plt.ylabel('angular velocity (rad/s)')

# plt.figure(3)
# plt.plot(time_steps, kinetic_energy, label='kinetic energy') # plotting kinetic energy
# plt.plot(time_steps, potential_energy, label='potential energy') # plotting potential energy
# plt.plot(time_steps, total_energy, label='total energy') # plotting total energy
# plt.xlabel('time (s)')
# plt.ylabel('energy (J)')
# plt.legend()
plt.show()
