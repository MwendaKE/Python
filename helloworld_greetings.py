import re


def get_correct_gender(input):
    if re.match("M|MALE", input, re.I):
        return "MR."
        
    elif re.match("F|FEMALE", input, re.I):
        return "MISS."
       
    else:
        return ""
        
print() 
       
user_name = str(input(" > What is your name: ")).upper()
gender = get_correct_gender(str(input(" > What is your gender? (M or F): ")))

print()

print(f" > HELLO WORLD, {gender} {user_name}.")
