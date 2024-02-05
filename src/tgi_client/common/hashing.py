import random  
import string  

length = 12
def hashing(): # define the function and pass the length as argument  
    # Print the string in Lowercase  
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length))) # run loop until the define length  
    return result