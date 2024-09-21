from pymongo import MongoClient


def get_database():
    client = MongoClient('localhost', 27017)

    db = client.tumaini.db
    
    return db

def add_student(name, adm, gender, yob, dorm):
    db = get_database()
    student_collection = db.students
    
    data = {
        "adm": adm,
        "name": name,
        "gender": gender,
        "yob": yob,
        "dorm": dorm
    }
    
    added = student_collection.insert_one(data)
    
    return added
    
def get_student(adm):
    db = get_database()
    
    student_collection = db.students
    
    student = student_collection.find_one({"adm": adm})
    
    return student
    
def edit_student(adm, name, gender, yob, dorm):
    db = get_database()
    
    student_collection = db.students
    
    student = student_collection.update_one({"adm": adm}, {"$set": {"name": name, "gender": gender, "yob": yob, "dorm": dorm}})
    
    return student.modified_count
    
def print_all_students():
    db = get_database()
    
    student_collection = db.students
    
    students = student_collection.find()
    
    return students
    
def delete_student(adm):
    db = get_database()
    
    student_collection = db.students
    
    student = student_collection.delete_one({"adm": adm})
    
    return student
    
    
def print_menu():
    print("  1. Add Student,")
    print("  2. Find Student,")
    print("  3. Delete Student,")
    print("  4. Edit Student,")
    print("  5. Print Students,")
    print("  6. Close Program,")
    print("  0. Show Menu,")
    
    return
    
print(" > STUDENT DATA COLLECTOR < ")
print()
print_menu()
print()

while True:
    print()
    menu_choice = int(input(" > Enter Choice: "))
    print()
    
    if menu_choice == 1:
        print(" > Add Student <")
        print()
        name = str(input("  ✓ Student Name: "))
        adm = str(input("  ✓ Admission Number: "))
        gender = str(input("  ✓ Gender (M or F): "))
        yob = str(input("  ✓ YOB (yyyy): "))
        dorm = str(input("  ✓ Dorm / Hostel: "))
        print()
        
        if name and adm and gender and yob and dorm:
            add = add_student(name, adm, gender, yob, dorm)
            
            if add:
                print(f"  + Added student with ADM No. {adm} | Query Id. {add.inserted_id}")
    
        else:
            print()
            print("  ! Error adding student!")
            
            continue
            
    elif menu_choice == 2:
        print(" > Find Student <")
        print()
        adm = str(input("  ✓ Enter Adm No: "))
        print()
        
        student = get_student(adm)
        
        if student:
            for key, value in student.items():
                print(f"  > {key}: {value}")
            
        else:
            print(f"  > No student with ADM {adm}.")
            
    elif menu_choice == 3:
        print(" > Delete Student <")
        print()
        adm = str(input("  ✓ Enter Adm No: "))
        print()
        
        student = get_student(adm)
        
        if student:
            del_prompt = str(input(f"  ! Delete °{student['name']}° ADM °{student['adm']}°? (Y or N): "))
        
            if del_prompt == "Y" or del_prompt == "y":
                delete = delete_student(adm)
                if delete:
                    print("  > Delete successful!")
                
                else:
                    print("  > Error deleting student!")
                
            else:
                print("  > Invalid input!")  
                
        else:
            print(f"  > No student with ADM {adm}.")
                 
    elif menu_choice == 4:
        print(" > Edit Student <")
        print()
        adm = str(input("  ✓ Enter Adm No: "))
        print()
        
        student = get_student(adm)
        
        if student:
            import re
            
            print(f"  ! Edit °{student['name']}° ADM °{student['adm']}°:")
            print()
            name = str(input(f"  *Change Name [{student['name']}]> "))
            gender = str(input(f"  *Change Gender [{student['gender']}]> "))
            yob = str(input(f"  *Change YOB [{student['yob']}]> "))
            dorm = str(input(f"  *Change Dorm [{student['dorm']}]> "))
            
            if name == "" or name.isspace() or not re.search("[\w+]\s[\w+]", name):
                name = student['name']
                
            if gender == "" or len(str(gender)) != 1:
                gender = student['gender']
                
            if yob == "" or len(str(yob)) != 4:
                yob = student['yob']
                
            if dorm == "":
                dorm = student['dorm']
              
            edit = edit_student(adm, name, gender, yob, dorm)
              
            if edit > 0:
                print()
                print("  + Student edited successfully.")
                
            else:
                print()
                print("  - Student not editted.")
                  
        else:
            print(f"  > No student with ADM {adm}.")
    
    elif menu_choice == 5:
        print(" > All Students <")
        print()
        students = print_all_students()
        
        for student in students:
            print(f"  #{student['name']}#")
            for key, value in student.items():
                print(f"   - {key}: {value}")
                if key == "name":
                    continue
                
            print()
            
    elif menu_choice == 6:
        import sys
        
        print(" > Program Shutdown <")
        sys.exit()
        
    elif menu_choice == 0:
        print_menu()
        
    else:
        continue
        
        
            
        



    
