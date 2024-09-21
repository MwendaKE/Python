# MwendaKE Programs
# https://github.com/MwendaKE
# Email: erickmwenda256@gmail.com
# Phone: +254 702 623 729
# Phone: +254 799 678 038

import os
import sys


def find_copies(directory):
    copies = []
    notcopies = []
    
    for f in os.listdir(directory):
        f = os.path.join(directory, f)
        
        if os.path.isfile(f) and "_copy" in f.lower():
            copies.append(f)
            
        else:
            notcopies.append(f)
            
    return copies, notcopies
    

while True:
    print(" " + "-" * 30)
    folder = str(input(" [+] Enter Target Folder (Q to Quit): "))
    print(" " + "-" * 30 + "\n")
    
    if folder == "Q":
        print(" [-] Program Shutdown!")
        
        sys.exit() 
        
    if os.path.isdir(folder):
        try:
            copies, notcopies = find_copies(folder)
            
            if copies:
                print("  [*] " + str(len(copies)) + " files to be removed:")
                for copy in copies:
                    print("   - " + str(copy))
                    
                remove_file_prompt = str(input("\n  [!] Remove files? Yes (Y) or No (N): "))
                
                if remove_file_prompt == "Y": 
                    print("")
                    for f in copies:
                        os.remove(f)
                        print("  [*] Removed " + str(f))
                        
                else:
                    print("  [-] Removing files cancelled!\n")
                    continue
    
            else:
                print(" [!] Sorry there are no copies!")
                print(" [!] Folder has " + str(len(notcopies)) + " files. \n")

        except Exception as e:
            print(" [-] Failed to remove: " + str(f) + "\n")

        
    else:
        print(" [+] Invalid Folder! \n")
        
        continue
       
        
# MwendaKE Programs
# https://github.com/MwendaKE
# Email: erickmwenda256@gmail.com
# Phone: +254 702 623 729
# Phone: +254 799 678 038