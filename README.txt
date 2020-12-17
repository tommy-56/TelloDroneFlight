TelloGame.py
DJI Tello drone flight control with an Xbox 360 controller
Fly the Tello with an Xbox controller with video feed coming through your connected computer
Tested with Python 3.6 and 3.7

Install
pip install -r requirements.txt

Usage
python TelloGame.py
No special command line arguments

Controls
A: Gain Altitude
X: Lose Altitude
Y: Take off
B: Land

Left Bumper: Pan left
Right Bumper: Pan Right

Left Stick: Forwards and backwards movement
Right Stick: Left and right movements

K: Quit Program

Future Development Notes
- Add the ability to take a recording or picture from the drone and save it



Credits
The original idea of controlling the Tello with a PC using the keyboard came from Damià Fuentes Escoté's TelloSDKPy script on github
My code has been adapted from his original script if you want to learn more please check it out


Notes for Xbox Controller on input values and button maps

Try tollerance as +-0.25 to start

Left Joy Stick = Driectional Left Right Forwards Backwards
Motion Full Up = -1
Motion Full Down = 1
Center  = 0   Note Tollerance needed maybe +-0.25 in any direction to get action
Motion Full Left  = -1
Motion Full Right = 1

Button Map
ABXY{
A: Gain Alt
X: Lose Alt
Y: Take off
B: Land
}

Trigers{
Left: None
Right: None
}

Bumpers{
Rotate control
Left: Pan Left
Right: Pan Right

}

Sticks{
Left: Driectional
Right: None # Maybe rotation later
}

ABXY = Button up/ Button down  response
Bumpers  = Button up/ Button down  response
Trigers = Same scale as joy sticks -1 - 1
