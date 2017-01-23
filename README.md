# Terrain Relative Navigation

## General
The full program is located in the _src_ package. Important to note is that not all the code in the various modules are used
 in the actual program, these are also indicated in comments. These were attempts to improve the code, however did not
 yield the desired results. Also, a full implementation of Neural Networks can be found in the NeuralNetwork package, unfortunately
 this is also not used for various reasons.
## Build information
###Required packages
numpy, os, pickle, PIL, matplotlib and scipy.

###Execution
This code is tested to execute successfully when launching a linux and windows terminal. 

There is, however, a known issue when executing the code from a IDE like PyCharm i.e. that it does not 
 recognize the data folders.

#### Terminal
*This program is run via the terminal by default*
For executing the entire program and viewing the crater detection and TRN on all the images, issue the following command: 

`python Main.py`

For executing the code on one image of choice (e.g. Scene1) issue the following command:

`python Main.py Scene1`

To execute the program on multiple images (e.g. Scene1 and Scene 3) issue the following command: 

`python Main.py Scene1 Scene3`

#### Execution from IDE
For execution from an IDE a slight manual modification in the Main.py file is required. Simply change
the line: 

`datapath = "data/"`

to 

`datapath = "../data/"`

For excecution of crater detection algorithms on images first import the crater detection module: 

`import src.CraterDetector as craterdetector`

and then one can use crater detection on the desired image:

`craterdetector.extractCratersWithImage(Image.open(datapath + "TRN/Angle1.ppm"))`

Note: the script above shows the result in an image. Using extract crater will not show any visuals.

