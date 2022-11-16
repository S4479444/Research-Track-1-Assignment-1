# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# -																										- #
# -                                                             ASSIGNMENT #1 - GIORDANO EMANUELE - MATR.: 4479444												- #
# -																										- #
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

########################################## THE CURRENT README.md IS REGARDING THE ASSIGNMENT ONLY; THE WHOLE PROJECT'S README.md IS IN THE FOLLOWING PATH: ####################################################
#																										  #
# 	This README.md contains only the information about the assignment #1. For any other informations about the main code, or the structure of the robot, tokens and the arena, please refer to:		  #
#				https://github.com/S4479444/Research-Track-1-Assignment-1/blob/main/README.md													  #
#																										  #
# 																										  #
###############################################################################################################################################################################################################

This project consists in a programmed mobile robot, that spawns in the upper left corner of a square arena. Inside the arena, there are placed a certain number of silver tokens, and an equal number of
golden tokens; the silver tokens are placed in the inner part of the arena, while the golden tokens are placed in the outer part. The goal of the mobile (holonomic) robot is to:

	1)	search for silver tokens in the whole arena, and saves the number of tokens in the arena, that the robot could see during scan;

	2) 	drive itself to the closest silver token in its sight;

	3)	once the robot is close to the targeted silver token, it grabs the token;

	4)	drive itself to the nearest golden token;

	5)	once the robot is close the targeted golden token, it releases the silver token that's been holding since point (3);

	6)	repeat, for all tokens in the arena.


In order to run the script, use the following syntax in OS terminator:
	
	$ python2 run.py assignment.py


# ----------------------------------------------------------------------------------- Functions ------------------------------------------------------------------------------------------------------------- #

In the first part of the file "assignment.py", the following functions are defined:
	
	1) drive(speed,seconds): 
		
		Info: 	This function drives the robot forward at a certain speed, and the robot stays in motion for a specified amount of time (seconds). It takes as inputs, the speed at which we want
			to drive the motor, and the delta_t for the linear motion; its output is the linear motion of the robot.
		
		Inputs: speed (float)	- the speed of linear motion							Output: The robot moves at speed <speed> for <seconds> seconds.
			seconds (float) - how long the robot will drive forward
			
	2) turn(speed,seconds)
	
		Info: 	This function turn the robot around its center. It takes as inputs the speed at which we want our robot to rotate, and the time interval for the "linear" rotation (with no
			angular acceleration); its output is the robot turning around its center.
			
		Inputs: speed (float)   - the speed of rotation (positive values for right turn,			Output: The robot will turn right or left, at speed <speed>, for <seconds> seconds.
						negative for left turn)
			seconds (float) - how long the robot will turn
	
	3) circle(speed, delta_speed, seconds)
	
		Info:	This function makes the robot move in a circular motion, which is composed both of a linear velocity component and an angular one. In order to do this, the function takes as
			inputs: the linear velocity component, which will be given to each motor; another speed parameter, which will be given only to one of the motors; and a time interval, that tells
			the robot how long has to hold the "drive" commands.
		
		Inputs: speed (float)       - the speed of linear motion component					Output: The robot moves of circular motion (one motor drives the robot forward,
			delta_speed (float) - the increment given to one of the motors, to make circular			at speed <speed> + <delta_speed> for <seconds> seconds, while the other
						motion										motor will drive the robot forward at speed <speed> for <seconds> seconds.
		
		
		Code:
			R.motors[0].m0.power = speed + delta_speed
			R.motors[0].m1.power = speed
			time.sleep(seconds)
			R.motors[0].m0.power = 0
			R.motors[0].m1.power = 0

			
	4) unique(list1)
	
		Info:	This function takes a list as input, and outputs another list, which contains the unique elements of the input list.
		
		Input: list1 (list)	- a generic list of elements							Output: unique_list (list) - the list of all unique elements of list1
		
	5) scan_token()
		
		Info:	This function scans the arena for silver tokens, since they are the primary target of our robot. The robot is programmed to turn around a couple of times, and scan
			the arena for silver tokens. In total, the robot is programmed to receive 15 "turn(speed,seconds)" commands, and the same number of searches; everytime the robot searches
			the arena, it stores every silver token's offset in its sight. Then, the list of all offsets (which includes repetitions - the robot might see, as it's turning around, the
			same token more than once) is given to the "unique(list1)" function (described above), that outputs the list of the actual tokens' offsets in the arena.
			
		Input: - - -							Output: token_unique_list (list) - the list of all unique tokens' offsets the robot has seen during the scan
		
		Pseudocode:
		
			def scan_token():
			
				initialize empty token list (token_list)
				define number of scans (n_scan)
				initialize loop variable (i)
				threshold distance for robot vision (dist)
				
				while i < n_scan
					turn around
					for every token in robot's sight
						if (token.dist is less than the threshold distance) and (token is silver)
							then add the token's offset to token_list
					i++
				
				call unique(token_list) function
				
				return unique_token_list
		
	5) find_silver_token(silver_list)
	
		Info:	This function's purpouse is to find the closest silver token in robot's sight, by taking as input the list of all silver tokens' offsets, of those that have already been placed
			correctly, near a golden token. Its output is a list of three element: the first is the closest silver token's distance, the second is the angle between the robot's y axis and
			the closest silver token, and the latter is the offset of the closest golden token. All elements are returned as -1, if the conditions are not met (either tokens are too far away, or
			there are only golden tokens ahead, or all the silver tokens the robot sees have already been correctly placed).
		
		Input: silver_list (list) - the list of all the silver tokens the robot has already			Output: [dist, rot_y, offset]  (list) 
						correclty placed (and must not be touched again)				The closest token in robot sight, that's not already been placed 
																near a golden token. Position 0 is for the distance, from the robot to the
																token; pos. 1 is the angle within respect to the y axis; pos. 2 is the
																token's offset (token.info.offset).
																
		Pseudocode:
		
			def find_silver_token(silver_list):
			
				define threshold distance for robot's vision (dist) to 100 (default)
				
				for every token in robot's sight	
					if (token_dist is less than dist) and (token_marker_tipe is SILVER) and (token_offset is not on the list of the already-placed silver tokens)
						then:
							dist = token_dist
							angle = token_angle 
							offset = token_offset
				
				if no silver token in sight (or already in the list)
					then return [-1, -1, -1]
				else
					return [dist, angle, offset]
			
	
	6) find_golden_token(golden_token_list)
	
		Info:	This function's purpouse is to find the closest golden token in robot's sight, by taking as input the list of all golden tokens' offsets, of those the robot has already placed a
			silver token aside them correctly. Its output is a list of three element: the first is the closest golden token's distance, the second is the angle between the robot's y axis and
			the closest golden token, and the latter is the offset of the closest golden token. All elements are returned as -1, if the conditions are not met (either tokens are too far away, or
			there are only silver tokens ahead, or all the golden tokens the robot sees have already been correctly welcomed a silver one.
		
		Input: golden_list (list) - the list of all the golden tokens the robot has already			Output: [dist, rot_y, offset]  (list) 
						correclty placed (and must not be touched again)				The closest token in robot sight, that's not already been placed 
																near a golden token. Position 0 is for the distance, from the robot to the
																token; pos. 1 is the angle within respect to the y axis; pos. 2 is the
																token's offset (token.info.offset).
																
		Pseudocode:
		
			def find_golden_token(golden_token_list):
			
				define threshold distance for robot's vision (dist) to 100 (default)
				
				for every token in robot's sight	
					if (token_dist is less than dist) and (token_marker_tipe is GOLD) and (token_offset is not on golden_token_list)
						then:
							dist = token_dist
							angle = token_angle 
							offset = token_offset
				
				if no golden token in sight (or already in the list)
					then return [-1, -1, -1]
				else
					return [dist, angle, offset]
			

	7) avoid_token(silver_token_list)

		Info:	This function makes the robot avoid obstacles, in particular silver tokens. When this function is called, it takes the list of all silver tokens that have already been placed,
			and checks there are silver tokens if in robot's sights, that are not on the list. Whenever the robot is close enough (threshold distance), then the robot is set in motion by two
			"circle" commands, once in the opposite direction of the token (depending on its orientation) and the other one to make the robot move back to it's orientation.
			The value for threshold distance has been chosen according to empirical sperimentation.
			
		Input:	silver_token_list (list)  - the list of all silver tokens that have already			Output: The robot avoid the obstacle.
							been placed correctly.		
	
	
		Pseudocode:
			
			def avoid_token(silver_token_list):
			
				define threshold distance for avoiding obstacles (d_th_avoid = 0.75)
				
				for every token in robot's sight
					if (token_offset is not in silver_token_list) and (marker_type is silver) and (token_dist < d_th_avoid)
						
						if token_angle >= 0
							circle(right)
							circle(left)
						
						if token_anfle < 0
							circle(left)
							circle(right)
						
				
				
				
# ---------------------------------------------------------------------------------------------------- MAIN ------------------------------------------------------------------------------------------------- #

The first part of the main is made to scan the arena and look for silver tokens. This is done by calling the scan_token() function, which makes the robot turn around and scout the area for tokens.
Once the list of tokens have been created, a while loop is initialized, with it's iterative counter that stops the loop when it's equal to the length of the list (which is to say, the code executes an exact
number of cicles, equal to the number of tokens). Everytime a golden token is reached and the silver token is dropped, the counter is increased.


Pseudocode:

		define threshold for distance (d_th = 0.4)
		define threshold for angle (a_th = 2.0)
		define threshold for release token (d_th_gold = 0.6)
		
		token_list = scan_token()
	
		initialize silver_token_list (for silver tokens that have been placed)
		initialize golden_token_list (for golden tokens that have been reached)
	
		define loop variable i = 0
	
		while ( i is less than length of token_list):
		
			define golden_token_search = 0 (serching for silver)
			
			call find_silver_token(silver_token_list)
			
			if no available silver tokens are in sight:
				then spins until it founds one
			
			if silver_token_distance is less than d_th:
				then grab the token
				insert the grabbed token into the silver_token_list
				golden_token_search = 1 (searching for gold)
				
				while golden_token_search == 1:
					
					call find_golden_token(golden_token_list)
					
					if no available golden tokens are in sight:
						then spins the robot until it founds one
					
					if golden_token_distance is less than d_th_gold:
						then release silver token
						insert the reached golden token into the golden_token_list
						golden_token_search = 0 (back to silver)
						i++
						break
					
					if golden_token_angle is between + or - a_th:
						then drive the robot forward
					
					if golden_token_angle is more than +a_th:
						then turn left
						
					if golden token_angle is less than -a_th:
						then turn right
		
			if silver_token_angle is between + or - a_th:
				then drive the robot forward
			
			if silver_token_angle is more than +a_th:
				then turn left
			
			if silver_token_angle is less than -a_th:
				then turn right
			
	
