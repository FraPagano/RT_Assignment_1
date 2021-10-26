#-------------IMPORT LIBRARIES----------------------
from __future__ import print_function
import time

#-------------IMPORT CLASS ROBOT--------------------
from sr.robot import *

#-------------DEFINING GOLBAL VARIABLES-------------

""" float: Threshold for the control of the linear distance"""
a_th = 2.3
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" instance of the class Robot"""  
R = Robot()
""" int: Maximum distance that the robot must maintain from golden tokens""" 
gold_th=1
""" float: Threshold for the activation of the grab routine"""
silver_th=1.5

#-------------DEFINING FUNCTIONS-------------

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
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
    
     	   #the field of view for detectig silver token is restricted to an angle of -70, 70 degrees. 
     	   #In this way the robot can detect silver token just in front of it. 
     	   #This is useful for avoid the robot detecting silver token behind it.
  
	     dist=token.dist
	     rot_y=token.rot_y
    if dist==3:
	return -1, -1
    else:
   	return dist, rot_y
   	
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -40<token.rot_y<40: 
    
    #the field of view for detectig gold token is restricted to an angle of -40, 40 degrees. 
    #In this way the robot can detect gold token just in front of it.
    
	     dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def find_golden_token_left():
    """
    Function to compute the closest golden token distace on the left of the robot.

    Returns:
	dist (float): distance of the closest golden token on the left of the robot (-1 if no golden token is detected on the left of the robot)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
        #The (-105, -75) angle span is useful for detecting gold token on the left
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
   	
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   	
def find_golden_token_right():
    """
    Function to compute the closest golden token distace on the right of the robot.

    Returns:
	dist (float): distance of the closest golden token on the right of the robot (-1 if no golden token is detected on the right of the robot)
    """

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
         #The (75, 1055) angle span is useful for detecting gold token on the right
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   	
def grab_routine(rot_silver, dist_silver): 
    """
    Function to control the routine for grabbing the silver tokens    
    Arguments: 
    	rot_silver (float): angle between the robot and the closest silver token
    	dist_silver (float): distance from the closest silver token
    No returns.
    """   
    if dist_silver <= d_th: 
    	print("Found it!")
    	if R.grab():
	    print("Grabbed!")
	    turn(20, 3)
	    drive(15, 0.8)
	    R.release()
	    drive(-15,0.8)
	    turn(-20,3)
    elif -a_th<=rot_silver<=a_th:
	    drive(40, 0.5) 
	    print("Correct angle")
    elif rot_silver < -a_th: 
	    print("Left a bit...")
	    turn(-5, 0.3)
    elif rot_silver > a_th:
	    print("Right a bit...")
	    turn(+5, 0.3)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def turn_method(left_dist, right_dist, dist_gold):
	"""
	Function that implements the turn decision method
	Arguments: 
		left_dist (float): distance of the closest gloden token on the left of the robot
		right_dist (float): distance of the closest gloden token on the right of the robot
	No returns.	
	"""	
	print("Where's the wall?")	
	if left_dist>1.2*right_dist:
		print("The wall is on the right at a distance of: "+ str(right_dist))
		while dist_gold<gold_th:
			dist_gold=find_golden_token()
			turn(-10, 0.1)
			print("I'm turning left")
	elif right_dist>1.2*left_dist:
		print("The wall is on the left at a distance of:  "+ str(left_dist))
		while dist_gold<gold_th:
			dist_gold=find_golden_token()
			turn(10, 0.1)
			print("I'm turning right")
	else:
		drive(15,0.5)
		print("Left and right distances are similar, i'll go straight")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def main():
	while 1:  
			#Updating variables value for every while cycle
			
			dist_silver, rot_silver = find_silver_token()
			dist_gold=find_golden_token()
			left_dist=find_golden_token_left()
			right_dist=find_golden_token_right()
			print("dist_gold= "+ str(dist_gold))
			#Check if gold token are detected, if no gold token are detected go straight ahead.						
			if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
					print("I'll go straight ahead")
					drive(70,0.5)		
			#If gold token are detected, then check where the wall is			
			elif dist_gold<gold_th and dist_gold!=-1:
			#The robot decides where to turn
					turn_method(left_dist, right_dist, dist_gold)					
			if dist_silver<silver_th and dist_silver!=-1: 
			#If any silver token closer than silver_th is detected, the grab routine will start
		    		print("Silver is close")
		    		grab_routine(rot_silver, dist_silver)	
		    			    		    				
#-----------------main() CALL-------------------

main()
    	

	
	
	
	
	


	    		
		
	
		
		
			
	
	
	
