# Author: SecByteX | Date: 29 June 2025
# Project: Password Strength Checker
import requests as req
import hashlib
import re 

colors = [
    "\033[31m", #red
     #"\033[32m" ,#green
    "\033[33m" ,#yellow
    "\033[34m", #blue
    "\033[35m", #purple
]
reset= "\033[0m"

def print_output(o_defects,point):
    

    if len(o_defects) == 0 :
        print("\033[32mGreat! Your password passed all strength checks.\033[0m")
        return 

    colored_defects = [
        f"{colors[i% len(colors)]}{o}{reset}"
        for i,o in enumerate(o_defects)
    ]
    defects = colored_defects
    max_length = max(len(dfct) for dfct in  defects) 
    box_weight = max_length - 3

    print("+"+ "-"*(box_weight-2) +  "+")

    for defect in defects:
        print("| 🔸"+ defect.ljust(max_length) +" |")

    print("+"+"-"*(box_weight-2) + "+")

    print("Result:",end="")
    if point == 100:
        print("Very Strong")
    elif point == 80:
        print("Strong")
    elif point == 60:
        print("Not Strong")
    elif point == 40:
        print("Weak")
    else :
        print("Very Weak")

def check_strength(passwd):

    point = 0
    defects = []

    uppercase_letter = re.search(r'[A-Z]',passwd)
    lowercase_letter = re.search(r'[a-z]',passwd)
    other_letter =  re.search(r'[\W_]',passwd)
    numeric_letter = len(re.findall(r'[0-9]',passwd)) 
    length_pass = len(passwd) 
    if not uppercase_letter:
        defects.append( "Must contain at least one uppercase letter (A–Z)")
    else:
        point+= 20
    
    if not lowercase_letter:
        defects.append ("Must contain at least one lowercase letter (a-z)")
    else:
        point+=20
    
    if not other_letter:
        defects.append("It must include a special character (such as !, @, $, etc.)")
    else :
        point+=20
    

    if numeric_letter <= 0:
        defects.append("Add at least 1 number (0–9)")
    elif numeric_letter < 2 :
        defects.append("Add at least 2 numbers.")
    else:
        point+=20
    
    if length_pass < 8 :
        defects.append (f"Must be longer than {length_pass} characters (at least 8)")
    else:
        point+=20

    return defects,point


def check_pwned(password):

    m=hashlib.sha1()
    m.update(password.encode("UTF-8"))
    full_sha1_pass= m.hexdigest()

    first5=full_sha1_pass[:5]
    last_from5= full_sha1_pass[5:]

    url = "https://api.pwnedpasswords.com/range/" + first5

    try:
        resp=req.get(url,timeout=5)
    except req.ConnectionError:
        print("\nNo internet connection...Pwnage check failed!\n")
        return
    except req.Timeout:
        print("\nThe connection timed out...Pwnage check failed!\n")
        return

    Regex_Pattern = rf"(?<={last_from5.upper()+":"})\d*\b"
    pwned_response_list=re.findall(Regex_Pattern,resp.text)

    if len(pwned_response_list) == 0:
        print("\033[32mGood news — no pwnage found!"+reset)
    else:

        print("\033[31mOh no — pwned!"+reset)
        pwned_times="This password has been seen \033[34m"+ "{:,}".format(int(pwned_response_list[0])) +" \033[31mtimes before in data breaches!"
        print("\033[31m"+pwned_times+reset)




input("[INFORMATION] : CTRL + C.... for quit.\n Okay?")
while True: 
    password = input("\033[44m Enter password:\033[0m ")
    defects,point=check_strength(password)
    print_output(o_defects=defects, point=point)
    check_pwned(password=password)

