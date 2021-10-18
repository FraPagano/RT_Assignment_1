from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python2 run.py solutions/exercise3_solution.py

"""
a_th = 2.3
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""
R = Robot()
""" instance of the class Robot"""   
gold_th=1
silver_th=1.5
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
"""def r_distances():
	cont=0
	temp=0
    	dist=5
    	gold_list=[]
    	i=0
    	for token in R.see():
    		cont=cont+1
        	if token.dist <= dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
			gold_list.append(token.dist)	
		elif token.dist<0.8:
			print("torno 0")
			gold_list.append(0)
		if token.dist ==100 or token.dist==-1:
			print("torno gold_list[-1]")
			gold_list.append(gold_list[cont-1])
				
	for i in gold_list:
		temp=i
		i=temp+i
   	return i
   	
def l_distances():
	cont=0
	temp=0
    	dist=5
    	gold_list=[]
   	i=0
    	for token in R.see():
    		cont=cont+1
        	if token.dist <= dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
			gold_list.append(token.dist)
		elif token.dist<0.8:
			print("torno 0")
			gold_list.append(0)	
		if token.dist==100 or token.dist==-1:
			gold_list.append(gold_list[cont-1])
	for i in gold_list:
		temp=i
		i=temp+i
   	return i	"""
    
def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -70<token.rot_y<70:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==3:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -40<token.rot_y<40:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token_left():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
   	
def find_golden_token_right():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
   	
def grab_silver(rot_silver):
	print("Go grab silver")
	if R.grab(): # if we grab the token....
		print("Gotcha!")
		turn(20, 3.2)
		R.release()
		turn(-20,3.2)
    	elif -a_th<=rot_silver<=a_th:
    		drive(40, 0.5) 
    		print("Ah, that'll do.")
	elif rot_silver < -a_th: 
		print("Left a bit...")
		turn(-5, 0.3)
	elif rot_silver > a_th:
		print("Right a bit...")
		turn(+5, 0.3)
   	


while 1:  
	dist_silver, rot_silver = find_silver_token()
	dist_gold, rot_gold =find_golden_token()
	left_dist=find_golden_token_left()
	right_dist=find_golden_token_right()
								
	if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
		print("Vado dritto")
		drive(70,0.5)		
					
	elif dist_gold<gold_th and dist_gold!=-1:

		print("Fermati, dov'e` il muro?")
    		
		if left_dist>right_dist:
			turn(-25, 0.3)
			print("Muro a destra "+ str(right_dist)+ ", la somma a sinistra invece e': "+str(left_dist))		
		elif right_dist>left_dist:
			turn(25, 0.3)
			print("Muro a sinistra "+ str(left_dist)+ ", la somma a destra invece e': "+str(right_dist))
		else:
			print("sinistra e destra circa uguali")
			print("destra: "+ str(right_dist))
			print("sinistra: "+str(left_dist))
			
			
	if dist_silver<silver_th and dist_silver!=-1: 
		print("Silver is close")
		if dist_silver < d_th: 
			print("Found it!")
			#grab_silver(rot_silver)
			
			if R.grab(): # if we grab the token....
			    	print("Gotcha!")
			    	turn(20, 3)
			    	R.release()
				turn(-20,3)
    		elif -a_th<=rot_silver<=a_th:
    			drive(40, 0.5) 
    			print("Ah, that'll do.")
	    	elif rot_silver < -a_th: 
			print("Left a bit...")
			turn(-10, 0.3)
	    	elif rot_silver > a_th:
			print("Right a bit...")
			turn(+10, 0.3)


	
	
	
	
	


	    		
		
	
		
		
			
	
	
	
