import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from tkinter import * # Import tkinter
import math


    

class pendulam:
    def __init__(self):
#   theta has range (-12 to +12) thetadot has range(-41.6,41.6) ,
#   * current has a range of [-12.8,12.8] in amp
        self.x_theta = np.arange(-12, 12.1, 0.1)
        self.x_thetadot = np.arange(-41.6, 41.7, 0.1)
        self.x_current  = np.arange(-12.8, 12.9, 0.1)
        self.fuzzy_mem_gen()
        
        
    def fuzzy_mem_gen(self):
# Generate fuzzy membership functions
        self.theta_zero = fuzz.trimf(self.x_theta, [-3, 0, 3])#tringular membership function
        self.theta_pos_small = fuzz.trapmf(self.x_theta, [0, 3, 9, 12])#trapizoidal membership function
        self.theta_neg_small = fuzz.trapmf(self.x_theta, [-12, -9, -3,0])
        self.thetadot_zero = fuzz.trimf(self.x_thetadot, [-10.4, 0, 10.4])
        self.thetadot_pos_small = fuzz.trapmf(self.x_thetadot, [0, 10.4, 31.2, 41.6])
        self.thetadot_neg_small = fuzz.trapmf(self.x_thetadot, [-41.6, -31.2, -10.4, 0])
        self.current_zero = fuzz.trimf(self.x_current, [-1.4, 0, 1.4])
        self.current_pos_small = fuzz.trapmf(self.x_current, [0, 1.4, 4.2, 5.6])
        self.current_pos_med = fuzz.trapmf(self.x_current, [3.6, 6.4, 10.6,12.8])
        self.current_neg_small = fuzz.trapmf(self.x_current, [-5.6, -4.2, -1.4, 0])
        self.current_neg_med = fuzz.trapmf(self.x_current, [-12.8, -10.6, -6.4, -3.6])
        


    def _visualize(self):
# Visualize these u membership functions
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

        ax0.plot(self.x_theta, self.theta_zero, 'b', linewidth=1.5, label='zero')
        ax0.plot(self.x_theta, self.theta_pos_small, 'g', linewidth=1.5, label='Positive Small')
        ax0.plot(self.x_theta, self.theta_neg_small, 'r', linewidth=1.5, label='Negative Small')
        ax0.set_title('Theta')
        ax0.legend()

        ax1.plot(self.x_thetadot, self.thetadot_zero, 'b', linewidth=1.5, label='zero')
        ax1.plot(self.x_thetadot, self.thetadot_pos_small, 'g', linewidth=1.5, label='Positive Small')
        ax1.plot(self.x_thetadot, self.thetadot_neg_small, 'r', linewidth=1.5, label='Negative Small')
        ax1.set_title('Theta.dot')
        ax1.legend()

        ax2.plot(self.x_current, self.current_zero, 'b', linewidth=1.5, label='Zero')
        ax2.plot(self.x_current, self.current_pos_small, 'g', linewidth=1.5, label='Positive Small')
        ax2.plot(self.x_current, self.current_pos_med, 'r', linewidth=1.5, label='Positive Medium')
        ax2.plot(self.x_current, self.current_neg_small, 'y', linewidth=1.5, label='Negative Small')
        ax2.plot(self.x_current, self.current_neg_med, 'm', linewidth=1.5, label='Negative Medium')

        ax2.set_title('Current')
        ax2.legend()
        
        # to turn off top-right axes
        for ax in (ax0, ax1, ax2):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        plt.tight_layout()
        plt.show()

    def fuzz_controller(self,theta,thetadot):
        count=0
        while (theta !=0 and thetadot !=0)and count<100 :
            if count== 0:
                Q=MainGUI()# OBJECT IS CREATED ONCE AND REUSED AFTER THAT
            Q.canvas.delete("pendulum")
            Q.displayPendulum(theta)
            Q.canvas.after(200) # Sleep for 200 milliseconds
            Q.canvas.update()
            self.fuzz_fit(theta,thetadot)
            current=self.fuzz_rule_defuzz()
            #print(current)
            
            (theta,thetadot)= _calculation_withg(current,theta,thetadot)
          #  (theta,thetadot)= _calculation(current,theta,thetadot)
            print(theta,thetadot,current)
            #print("thetadot",thetadot)
            #print("current",current)
            count+=1

    def fuzz_fit(self,theta,thetadot):
#obtaining membership value by fitting theta, and thetadot to membership functions
        self.theta_zero_mvalue = fuzz.interp_membership(self.x_theta, self.theta_zero, theta)
        self.theta_neg_small_mvalue = fuzz.interp_membership(self.x_theta, self.theta_neg_small, theta)
        self.theta_pos_small_mvalue = fuzz.interp_membership(self.x_theta, self.theta_pos_small, theta)

        self.thetadot_zero_mvalue = fuzz.interp_membership(self.x_thetadot, self.thetadot_zero, thetadot)
        self.thetadot_neg_small_mvalue = fuzz.interp_membership(self.x_thetadot, self.thetadot_neg_small, thetadot)
        self.thetadot_pos_small_mvalue = fuzz.interp_membership(self.x_thetadot, self.thetadot_pos_small, thetadot)


    def fuzz_rule_defuzz(self):
    #1. Rule 1
        rule1 = np.fmin(self.theta_neg_small_mvalue, self.thetadot_neg_small_mvalue)
        current_pos_med1 = np.fmin(rule1, self.current_pos_med)
    #2. Rule 2
        rule2 = np.fmin(self.theta_zero_mvalue, self.thetadot_neg_small_mvalue)
        current_pos_small1 = np.fmin(rule2, self.current_pos_small)
    #3. Rule 3
        rule3 = np.fmin(self.theta_pos_small_mvalue, self.thetadot_neg_small_mvalue)
        current_zero1 = np.fmin(rule3, self.current_zero)
    #4. Rule 4
        rule4 = np.fmin(self.theta_neg_small_mvalue, self.thetadot_zero_mvalue)
        current_pos_small2 = np.fmin(rule4, self.current_pos_small)
    #5. Rule 5
        rule5 = np.fmin(self.theta_zero_mvalue, self.thetadot_zero_mvalue)
        current_zero2 = np.fmin(rule5, self.current_zero)
    #6. Rule 6
        rule6 = np.fmin(self.theta_pos_small_mvalue, self.thetadot_zero_mvalue)
        current_neg_small1 = np.fmin(rule6, self.current_neg_small)
    #7. Rule 7
        rule7 = np.fmin(self.theta_neg_small_mvalue, self.thetadot_pos_small_mvalue)
        current_zero3 = np.fmin(rule7, self.current_zero)
    #8. Rule 8
        rule8 = np.fmin(self.theta_zero_mvalue, self.thetadot_pos_small_mvalue)
        current_neg_small2 = np.fmin(rule8, self.current_neg_small)
    #9. Rule 9
        rule9 = np.fmin(self.theta_pos_small_mvalue, self.thetadot_pos_small_mvalue)
        current_neg_med1= np.fmin(rule9, self.current_neg_med)

    #############################################
    # Aggregate individual membership functions
        current_zero_final=np.fmax(np.fmax(current_zero1, current_zero2),current_zero3)
        current_pos_med_final=current_pos_med1
        current_neg_med_final=current_neg_med1
        current_pos_small_final=np.fmax(current_pos_small1, current_pos_small2)
        current_neg_small_final=np.fmax(current_neg_small1, current_neg_small2)
    # Overall aggregate function
        aggregate =  np.fmax(current_zero_final,np.fmax(np.fmax(current_pos_med_final,current_neg_med_final),np.fmax(current_pos_small_final,current_neg_small_final)))
    #DEfuzzification centroid method
        current = fuzz.defuzz(self.x_current, aggregate, 'centroid')
        return(current)
    #print(current)
    #(theta,thetadot)= _calculation(current,theta,thetadot)
    #print(theta)
    #print(thetadot)

class MainGUI:
    def __init__(self):
        self.window = Tk() # Create a window, we may call it root, parent, etc
        self.window.title("Pendulum") # Set a title

        self.canvas = Canvas(self.window, bg = "white", width = 200, height = 200)
        self.canvas.pack()
        self.delay = 200
       
    def displayPendulum(self,angle):
        x1 = 100;
        y1 = 200;
        rodRadius = 150
        bobRadius = 10
        x = x1 + rodRadius * math.cos(math.radians(90 -angle))
        y = y1 - rodRadius * math.sin(math.radians(90 -angle)) #to make verticle

        self.canvas.create_line(x1, y1, x, y, fill="blue", tags = "pendulum")
        self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, 
                                fill = "green", tags = "pendulum")
        self.canvas.create_oval(x - bobRadius, y - bobRadius, 
                                x + bobRadius, y + bobRadius,
                                fill = "red", tags = "pendulum")


def _calculation(i,theta,thetadot):
    k=20;dt=0.2;m=1;d=1
    I=m*d*d
    tau=k*i
    thetadotdot=(tau/I)
    
    delthetadot=thetadotdot*dt
    thetadot= thetadot + delthetadot
    
    deltheta = thetadot*dt
    theta= theta + deltheta
    return(theta,thetadot)

def _calculation_withg(i,theta,thetadot):
    k=20;dt=0.2;m=1;d=1;g=10
    I=m*d*d
    tau=k*i
    thetadotdot=(tau/I)+(g/d)*math.sin(math.radians(theta))
    
    delthetadot=thetadotdot*dt
    thetadot= thetadot + delthetadot
    
    deltheta = thetadot*dt
    theta= theta + deltheta
    return(theta,thetadot)





######################################

theta=float(input("provide inout theta value: "))
thetadot=float(input("provide inout thetadot value: "))
P=pendulam()
P._visualize()
P.fuzz_controller(theta,thetadot)









