from __future__ import print_function

import numpy
import time

from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_gold_th = 0.6
""" float: Threshold for the control of linear distance (golden tokens)"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

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


def circle(speed, delta_speed, seconds):
    """
    Function for setting circular motion
    
    Args: speed (int) - the speed of the wheels
	  seconds (int) - the time interval
    
    delta_speed is the variation we give to one
    motor (here, is m0) in order to make the robot
    turn, but, at the same time, have a linear velocity component
    """
    R.motors[0].m0.power = speed + delta_speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    


def unique(list1):

	unique_list = []
	
	for x in list1:
		if x not in unique_list:
			unique_list.append(x)
			
	return unique_list	

def scan_token():
	
	print("Scanning for silver tokens...")
	token_list = []
	n_scan = 15
	i = 0
	dist = 100
	
	while i < n_scan:
		turn(50, 0.2)
		for token in R.see():
			if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
				token_list.append(token.info.offset)
		i = i + 1
	
	token_unique_list = unique(token_list)
	
	return token_unique_list
		

def find_silver_token(silver_token_list):
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.info.offset not in silver_token_list:
		dist=token.dist
		rot_y=token.rot_y
		offset = token.info.offset
    if dist ==100:
    	return [-1,-1,-1]
    else:
    	return [dist, rot_y, offset]



def find_golden_token(golden_token_list):
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.offset not in golden_token_list:
            dist=token.dist
	    rot_y=token.rot_y
	    offset = token.info.offset
    if dist == 100:
    	return [-1,-1,-1]
    else:
        return [dist, rot_y, offset]
        
        
        
def avoid_token(silver_token_list):
    """ 
    Function to avoid collisions with silver tokens.
    
    Input: 
    	silver_token_list (list): the list of all tokens that have already been grabbed
    	
    Returns:
    	move the robot
    """
    d_th_avoid = 0.75
    for token in R.see(): 
    	if token.info.offset not in silver_token_list and token.info.marker_type is MARKER_TOKEN_SILVER and token.dist < d_th_avoid:
    		print("Oh boy! There's a silver token in the way!")
    		if token.rot_y <= 0:
    			circle(50,40,0.4)
    			print("Let me turn...")
    			circle(50,-20,0.4)
    		if token.rot_y > 0:
    			circle(50,-40,0.4)
    			print("Let me turn...")
    			circle(50,20,0.4)
    			
    			

# ------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------- #

# ------------------------------ Scanning the Arena, to know the number of silver tokens ---------------------------- #




token_list = scan_token()
print("I can see ", len(token_list), " silver tokens in the arena!")
time.sleep(1)

silver_token_list = []
golden_token_list = []	

i = 0


while i < len(token_list):

	golden_token_search = 0											# It's time to search for silver tokens
	
	silver_token = find_silver_token(silver_token_list)								# First, the robot searches for the nearest silver token.
	
	if silver_token[0] == -1:											# If no silver token is found, then the robot starts spinning until it founds one
		print("I can't see any silver token!!")
		print("Let me drive until I find one")
		
		while silver_token[0] == -1:										# Spin the robot until it founds a silver token
			turn(-50,0.01)
			silver_token = find_silver_token(silver_token_list)
	
	if silver_token[0] < d_th:											# If the token is in grab distance
		print("Silver token is straight ahead!")
		R.grab()												# Grab!
		silver_token_list.insert(0,silver_token[2])								# Insert the grabbed token into the list, not to be touched again (after the placement)
		print("Gotcha!")
		print("Now bringing it to the corresponding golden token")
		golden_token_search = 1										# It's time to search for golden tokens
		
		while golden_token_search == 1:									# Until the golden token has been reached and silver token placed, then:
			
			golden_token = find_golden_token(golden_token_list)						# Find nearest golden token

			if golden_token[0] == -1:									# If no golden tokens are in sight
				print("I cant't see the golden token!!")
				print("Let me turn until I find one")
				while golden_token[0] == -1:								# Spin the robot until it founds a golden token
					turn(-50,0.01)
					golden_token = find_golden_token(golden_token_list)
		
			if golden_token[0] < d_gold_th:								# If golden token inside the threshold of R.release()
				print("Golden token is straight ahead")	
				R.release()										# Release!
				golden_token_list.insert(0, golden_token[2])						# Insert the reached golden token into the list, not to be reached again.
				print("Task completed!")
				print("Now searching for next silver token...")
				golden_token_search = 0								# Return to searching for silver tokens
				i = i+1
				break

		
			if -a_th <= golden_token[1] <= a_th:								# If the robot is well aligned with the token, then go forward
				print("Ah, here we are!")	
				drive(70,0.01)
				avoid_token(silver_token_list)
						
				
			elif golden_token[1]< -a_th:									# Golden token is too much on the left
				print("Left a bit...")
				turn(-7.5,0.01)
				
			elif golden_token[1] > a_th:									# Golden token is too much on the right
				print("Right a bit...")
				turn(7.5,0.01)
		
		
	elif -a_th <= silver_token[1] <= a_th: # If the robot is well aligned with the token, then go forward
		print("Ah, here we are!")
		drive(70, 0.01)
		
	elif silver_token[1] < -a_th:
		print("Left a bit...")											# Silver token is too much on the left
		turn(-7.5, 0.01)
	elif silver_token[1] > a_th:
		print("Right a bit...")										# Silver token is too much on the right
		turn(+7.5, 0.01) 


turn(100,0.7)
drive(100,1.25)
turn(100,3)
print("------ Mission completed! ------")
