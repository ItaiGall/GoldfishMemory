import string
import random

def RndStr():
    S = 4  # number of characters in the string.

    ran = ''.join(random.choices(string.ascii_letters + string.digits, k = S))
    #print("The randomly generated string is : " + str(ran))
    return ran