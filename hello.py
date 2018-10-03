#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Print a conventional message

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:   February 2018

First program hello.py: display "Hello, world!" on standard output.
"""


#import libraries: import <name> as <n>

#definition of functions
#def my_func(param1, param2):


#dictionary=[1:"k1", "k2":2]


import sys

# By convention, a function name must contain only lowercase characters and _.
# txt=None defines a default value for string and makes it optional.
def PrintMsg(txt=None):
    """Print a message received as an argument or a default message
    if none is passed.

    :param txt: a string to print (optional)
    :return: status value (always success, 0)
    """

    if txt is None:
        # Define a default message
        txt = 'Hello, world!'
    print("{}".format(txt)) # Will change the form of txt-parameter to string and then it will print it twice.
    # If txt is a number it will become first a string, f.i. 12 -> "12", and then it will print ==> 1212

    return 0




print("Hello, world!")
word="Hello, world!" #string variable
print(word*3)
num=1
t=2.
print(num/t)
print("!",t)


print(5/2) # complete deviation
print(5//2) # integer deviation
print(5 % 2) # rest of integer deviation

# for <counter> in range(start, end, step):
for i in range(0, 10, 1): # loop from 0 to 9
    # print("Hi",i)
    if i>8:
        print("greater",i)
    elif i==4:
        print("equal",i)

nlist=[1,2,3]
print(nlist)

print("")
print("=================")
print("")




# The following test is considered as a best practice: this way a module
# can be used both as a standalone application or as a module called by another
# module.

# if __name__ == "__main__":: pattern to allow a file to be either imported or run directly.
# For example, in this case the function print_msg() could be used by another module after importing this one.
if __name__ == "__main__":

    sent = "My name is Giorgos. "
    var2 = 10
    # The main program is implemented mainly as a function: this avoids having
    # all the variables used in this context (e.g. text in print_msg) to
    # become global variables.
    status = PrintMsg(var2+1)
    status = PrintMsg(var2)
    stat = PrintMsg(sent)

    sys.exit(stat)




print("---- DONE ----")