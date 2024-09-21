"""
Program will generate random passwords with a minimum length of 8 characters.
"""

import string
import random

def truncate_name(name):
    pass
    
def mix_name_case(name):
    mixed_case_list = []
    namelist = list(name)
    
    for letter in namelist:
        if namelist.index(letter) % 2 != 0:
            letter = letter.upper()
                
        else:
            letter = letter.lower()
                
        mixed_case_list.append(letter)
            
    mixed_case = "".join(mixed_case_list)
    
    return mixed_case
    
        
def generate_password(username):
    possible_password = []
    
    digits = list(string.digits)
    digits_choice = random.choice(string.digits)
    letters_choice = random.choice(list(string.ascii_uppercase))
    punctuations_choice = random.choice(list("&#!_@-$%=£"))
    
    min_pass_len = 8
    
    letter_design = random.choice([0, 1, 2, 3])
    
    if letter_design == 0:
        username = username.upper()
        
    elif letter_design == 1:
        username = username.lower()
        
    elif letter_design == 2:
        username = username.capitalize()
        
    else:
        username = mix_name_case(username)
    
    
    possible_password.append(username)
    possible_password.append(letters_choice)
    possible_password.append(punctuations_choice)
    possible_password.append(digits_choice)
    
    password = "".join(possible_password)
    
    if len(password) < min_pass_len:
        rem_len = min_pass_len - len(password)
        
        random.shuffle(digits)
        
        extra_chars = digits[:rem_len]
        
        possible_password.extend(extra_chars)
        
    random.shuffle(possible_password)
    
    password = "".join(possible_password)
    
    return password
        

print()

while True:
    print()      
    username = str(input(" > Enter Your First / Second Name: "))
    print()
    print(" > Possible Passwords: ")
    print()

    for i in range(10):
        password = generate_password(username)
        print(f" > Password: {password}")