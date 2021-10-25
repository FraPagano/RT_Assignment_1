Research Track 1, first assignment
================================

Introduction
--------------------------------

The first assignment of the [Research Track 1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) class is about a simple, portable robot simulator provided us by professor [Carmine Recchiuto](https://github.com/CarmineD8). 
As students, before starting doing the assignment, we were asked to do some training exercise in order to become acquainted with both the simulator and the program language python. In these excercises we had to make the robot do some simple movement but also grab some game object called "Tokens". Tokens are a sort of squares that could be silver or gold. 
Back to the assignment, we were supposed to make the robot move inside in the counter-clockwise direction in a predefinite circuit bordered by a set of gold Tokens without touching them. At the same time, whenever the robot detects silver Tokens inside the circuit, it should grab and move them behind itself. You can find the code I created at the following [link](https://github.com/FraPagano/RT_Assignment_1/blob/main/assignment.py)

Here's some pictures that shows the robot, the silver and the gold token that i was writing about:

###### Robot:

![immagine](https://github.com/FraPagano/RT_Assignment_1/blob/main/sr/robot.png)

###### Silver Token:

![immagine](https://github.com/FraPagano/RT_Assignment_1/blob/main/sr/token_silver.png)

###### Gold Token:

![immagine](https://github.com/FraPagano/RT_Assignment_1/blob/main/sr/token.png)


The circuit in which the robot should navigate is the following:

![immagine](https://github.com/FraPagano/RT_Assignment_1/blob/main/images_gifs/map.JPG)


The code I implemented is very simple but efficient, indeed I wrote just a few lines of code but these computes all the neccessary controls in order to make the robot navigate correctly. The idea is to make the robot go straight forward unless some gold or silver token are detected, depending on the tokens' color the robot does different things.

The greaest issues that I faced with during the implementation of the project were:
* design a turn decision method;
* create a code that does such turn decision method;
* find all the correct parameters (i.e. linear and angular velocity, duration time for `drive()` and `turn()` functions, threshold values, etc..) in such a way as not to be too fast or too slow.

Here's some useful informations regarding installing and running the simulator.

## Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

#### Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

#### Run the programs

To run one or more scripts in the simulator, use `run.py`, passing it the file names.
Example: `python2 run.py file_name.py`

Methods
----------------------

Here's some properties of the robot's class that I used for the assignment.

### Motors

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).


For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
These attributes were so much useful for my functions because thanks to them I could make the robot detect both silver and gold tokens in every direction. The mentioned funtions are:
* `drive(speed, seconds)`. This function allows the robot to move straight for a certain time interval with a determinated speed. The arguments of the function are:
  *  speed (int): the speed of the wheels
  *  seconds (int): the time interval

There are no return values
* `turn(speed, seconds)`. This function allows the robot to turn for a certain time interval with a determinated speed. The arguments of the function are:
  *  speed (int): the speed of the wheels
  *  seconds (int): the time interval
 
There are no return values
* `find_silver_token()`. This function helps the robot finding both the distance and the angle (between robot and token) of the closest silver token. An important thing to explain is that the sensors that the robot is equipped with can detect every token in the map in a 360 degrees field of view, so when the robot grabs and moves behind it the first silver token, actually this is still the closest silver token to detect. I avoided this issue by giving the robot a restricted field of view, so that it could only "see" tokens in front of him: from -70 up to 70 degrees at a maximum distance of 3 _meters_. By this way, once that the robot released the first silver token it goes for the next one. There are no arguments for this function. The return values are:
  *  dist (float): distance of the closest silver token (-1 if no silver token is detected)
  *  rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected) 
 
* `find_golden_token()`. That function does exactly the same thing of the previous one but with the gold token instead. I gave a restricted field of view in this case too, so that the robot can detect every gold token in a -30 up to 30 degrees' field of view. There are no arguments for this function. The return values are:
  *  dist (float): distance of the closest gold token (-1 if no gold token is detected)
  *  rot_y (float): angle between the robot and the gold token (-1 if no gold token is detected)

* `find_golden_token_left()`. This is the function that computes the distance of the closest gold token on the left of the robot. I could do that by giving the robot an additional and restricted field of view that goes from -105 up to -75 degrees. There are no arguments for this function. The return value is:
  *  dist (float): distance of the closest silver token on the left of the robot (-1 if no silver token is detected on the left of the robot)
* `find_golden_token_right()`. This is the function that computes the distance of the closest gold token on the right of the robot. I could do that by giving the robot an additional and restricted field of view that goes from 75 up to 105 degrees. There are no arguments for this function. The return value is:
  *  dist (float): distance of the closest silver token on the right of the robot (-1 if no silver token is detected on the right of the robot)
* `grab_routine(rot_silver, dist_silver)`. This function activates the routine for grabbing the detected silver token. It makes the robot allign, grab and release the token. The arguments of the function are:
  *  rot_silver (float): angle between the robot and the closest silver token
  *  dist_silver (float): distance from the closest silver token

There are no return values
* `turn_method(left_dist, right_dist)`. This function implements the turn decision method. The arguments of the function are:
  *  left_dist (float): distance of the closest gloden token on the left of the robot
  *  right_dist (float): distance of the closest gloden token on the right of the robot

There are no return values

For example, the following code prints the distances of the closest gold token on the left and on the right of the robot:
```python
def print_right_distance()
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
        #The (75, 105) angle span is useful for detecting gold token on the right
            dist=token.dist
   	print(dist)
      
         
def print_left_distance()         
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
        #The (-105, 75) angle span is useful for detecting gold token on the left
            dist=token.dist
   	print(dist)

print_right_distance()
print_left_distance()
```
In this way `find_golden_token_right()` and `find_golden_token_left()` helps the robot turning in the correct direction. The idea is to compute these distances everytime that the robot faces a wall. When the robot is in this condition it controls if the distance computed on the right is greater or smaller than the distance computed on the left. Actually, in order to make the robot turn when the difference between the two computed values is relevant I inserted a coefficient that contributes to increment their difference. By this way the robot only turns when the distances are significantly different, avoiding some wrong decisions. 

This is a pseudocode of the  turn decision method:
```python
  if dist_left>1.2*dist_right:  
    print "The wall is on the right, so turn left"
    turn_left
  elif dist_right>1.2*dist_left:
     print "the wall is on the left, so turn right"
    turn_right
  else:
    go_straight_ahead
 ```
Every parameter such as linear and angular velocity, duration time for `drive()` and `turn()` functions, threshold values, anglular span, etc.. have been found experimentally.

 ### Flowchart
For a more precise description of what my code does you can consult the following flowchart, created with [Lucidchart](https://www.lucidchart.com/pages/it/landing?utm_source=google&utm_medium=cpc&utm_campaign=_chart_it_allcountries_mixed_search_brand_bmm_&km_CPC_CampaignId=9589672283&km_CPC_AdGroupID=99331286392&km_CPC_Keyword=%2Blucidcharts&km_CPC_MatchType=b&km_CPC_ExtensionID=&km_CPC_Network=g&km_CPC_AdPosition=&km_CPC_Creative=424699413299&km_CPC_TargetID=kwd-334618660008&km_CPC_Country=1008337&km_CPC_Device=c&km_CPC_placement=&km_CPC_target=&mkwid=sKwFuAgHb_pcrid_424699413299_pkw_%2Blucidcharts_pmt_b_pdv_c_slid__pgrid_99331286392_ptaid_kwd-334618660008_&gclid=CjwKCAjw5c6LBhBdEiwAP9ejG86DblinG5ivYRvMmKSvI8Dl7as9i2oINlmgqIDoj0gpLX6WfnCenRoCxxQQAvD_BwE)

![immagine](https://github.com/FraPagano/RT_Assignment_1/blob/main/images_gifs/RT_first_assignment_flowchart.JPG)

Results
--------------------------------
In order to make you understand how my code works i created this video ![video](https://github.com/FraPagano/RT_Assignment_1/blob/main/images_gifs/4x_video.mp4)

