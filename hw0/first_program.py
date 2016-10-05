# This file, with a .py extension, contains a Python Program
# Lines that start with the hash sign are ignore by Python.
# they are used for comments. 

# Step 1: To run this program, in a terminal window, type:
# cd ~/Homeworks/hw0
# and then type "python first_program.py"
#
# If you aren't sure how to open a terminal window, look at the
# bottom left of Mint and find the box that looks like >_. Click.
#

def hello():
    print "--------------------------------"
    print "Welcome to HCDE 310."
    print ""
    print "We are glad you are here"
    print "and we hope you enjoy the class."
    print "--------------------------------"
    
hello()
print "... Let's say that again... \n"
hello()

# Step 2: Now try deleting the second hello(). Save the file.
# Run the program again to see the results.

# Step 3: Now insert "hello()" back into the editor buffer
# below this line. Try using the auto-complete feature. After 
# you type "hel", possible completions should appear.
# Use the arrow keys or the mouse to select, and hit enter.

# Save the file. Run it again to see the results. 

# Step 4: Now, try a Python program that uses variables. Uncomment
# the lines below, by removing the # at the start of each line. Fill
# in the values for length, width, height, and your name. 
# Then save and run the program again.

length = 1
width = 2
height = 3

me = "Anastasia"
print "Volume =", width*length*height
print "My name is",me

# Step 5: Instead of running the program from a terminal window,
# you can run it inside Eclipse. After you save it, click the run 
# icon in the ribbon (the green "play" button), or choose Run from
# the menu. The output will show up at the bottom of the screen, in
# the Console window.
