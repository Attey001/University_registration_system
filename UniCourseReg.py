import datetime

print("********** WELCOME TO THE SCHOOL REGISTRATION SYSTEM **********")

# Define courses by level and semester with credits
course_offerings = {
    (100, 1): ["FREN121: French", "ENGL111: Language I"],
    (100, 2): ["GNED100: Study Skills", "RELB163: Teachings of Jesus"],
    (200, 1): ["PEAC100: Physical Activity", "PSYC105: Psychology"],
    (200, 2): ["CMME115: Communication Skills", "RELB251: Christian Faith"],
    (300, 1): ["SOCI105: Social Science", "ENGL112: Language II"],
    (300, 2): ["HLTH561: Health Principles", "RELT383: Biblical Foundation"],
    (400, 1): ["MGNT211: Management", "AFST305: African Studies"],
    (400, 2): ["STAT134: Statistics", "GNED350: Career Planning"]
}

# Course credits information
course_credits = {
    "FREN121": 3, "ENGL111": 3, "GNED100": 2, "RELB163": 2,
    "PEAC100": 1, "PSYC105": 3, "SOCI105": 3, "ENGL112": 3,
    "CMME115": 3, "RELB251": 2, "HLTH561": 3, "RELT383": 3,
    "MGNT211": 3, "AFST305": 3, "STAT134": 4, "GNED350": 2
}

# Prerequisite courses
prerequisites = {
    "ENGL112": ["ENGL111"],
    "RELB251": ["RELB163"],
    "STAT134": ["MATH101"],
    "HLTH561": ["BIOL101"]
}

# Sample student academic history
student_academic_history = {
    "STU001": {
        "completed_courses": {
            "ENGL111": "A", "FREN121": "B", "GNED100": "A", 
            "RELB163": "B", "PEAC100": "A", "MATH101": "C"
        },
        "gpa": 3.2
    },
    "STU002": {
        "completed_courses": {
            "ENGL111": "B", "FREN121": "C", "GNED100": "B",
            "RELB163": "A", "BIOL101": "B"
        },
        "gpa": 2.8
    }
}

# Grade points mapping
grade_points = {
    "A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, 
    "C": 2.0, "D": 1.0, "F": 0.0
}

def get_student_info():
    """Get and validate student ID, level, and semester"""
    stud_id = input("Enter Student ID: ").strip().upper()
    print(f"\nWelcome, Student {stud_id}")
    
    # Display student GPA if available
    if stud_id in student_academic_history:
        gpa = student_academic_history[stud_id]["gpa"]
        print(f"Current GPA: {gpa:.2f}")
    else:
        print("New student - no academic record found")
    
    level = [100, 200, 300, 400]
    sem = [1, 2]
    
    print("Available Levels:", level)
    
    while True:
        try:
            slevel = int(input("Select your level: "))
            if slevel in level:
                break
            else:
                print("Invalid level. Please select from", level)
        except ValueError:
            print("Please input a numeric value (e.g., 100, 200).")
    
    print("Semesters Available:", sem)
    while True:
        try:
            ssem = int(input("Select your semester (1 or 2): "))
            if ssem in sem:
                break
            else:
                print("Invalid semester. Please choose 1 or 2.")
        except ValueError:
            print("Please input a numeric semester (1 or 2).")
    
    return stud_id, slevel, ssem

def check_prerequisites(student_id, course_id):
    """Check if student has completed prerequisite courses"""
    if course_id not in prerequisites:
        return True, []  # No prerequisites
    
    # Get completed courses, empty dict if student doesn't exist
    completed_courses = student_academic_history.get(student_id, {}).get("completed_courses", {})
    
    required_prereqs = prerequisites[course_id]
    missing_prereqs = []
    
    for prereq in required_prereqs:
        if prereq not in completed_courses:
            missing_prereqs.append(prereq)
    
    if missing_prereqs:
        return False, missing_prereqs
    else:
        return True, []

def display_courses(available_courses, student_id):
    """Display available courses for the semester with prerequisites info"""
    if available_courses:
        print("\nHere is the list of courses for the semester:")
        print("-" * 60)
        
        for i, course in enumerate(available_courses, 1):
            course_id = course.split(":")[0]
            credits = course_credits.get(course_id, "N/A")
            prereq_ok, missing_prereqs = check_prerequisites(student_id, course_id)
            
            # Display course with number
            print(f"{i}. {course} (Credits: {credits})")
            
            # Show prerequisite information
            if not prereq_ok:
                print(f"   ⚠️  Missing prerequisites: {', '.join(missing_prereqs)}")
            elif course_id in prerequisites:
                print(f"   ✅ Prerequisites met")
            else:
                print(f"   ✅ No prerequisites required")
                
        print("-" * 60)
    else:
        print("\nNo courses available for this level and semester.")

def calculate_tuition(registered_courses):
    """Calculate tuition fees based on registered courses"""
    credit_cost = 50  # Cost per credit hour
    total_credits = 0
    total_cost = 0
    
    for course_id in registered_courses:
        if course_id in course_credits:
            credits = course_credits[course_id]
            total_credits += credits
            total_cost += credits * credit_cost
    
    return total_credits, total_cost

def calculate_potential_gpa(student_id, new_courses):
    """Calculate potential GPA after adding new courses"""
    if student_id not in student_academic_history:
        return "N/A"  # No previous academic record
    
    current_record = student_academic_history[student_id]
    completed_courses = current_record["completed_courses"]
    
    # Assume average grade of B for new courses (for prediction)
    predicted_grades = {course: "B" for course in new_courses}
    
    # Combine completed and new courses
    all_courses = {**completed_courses, **predicted_grades}
    
    total_grade_points = 0
    total_credits = 0
    
    for course_id, grade in all_courses.items():
        if course_id in course_credits and grade in grade_points:
            credits = course_credits[course_id]
            grade_point = grade_points[grade]
            total_grade_points += credits * grade_point
            total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return total_grade_points / total_credits

def register_courses(available_courses, registered_courses, student_id):
    """Handle course registration with prerequisite checking"""
    if not available_courses:
        print("No courses available to register.")
        return registered_courses
    
    print("Enter Course ID of courses you want to register. Type 'done' when finished.")
    available_ids = [course.split(":")[0] for course in available_courses]
    print(f"Available Course IDs: {', '.join(available_ids)}")
    
    while True:
        course = input("\nEnter Course ID: ").strip().upper()
        if course == 'DONE':
            break
        elif course in available_ids:
            # Check prerequisites
            prereq_ok, missing_prereqs = check_prerequisites(student_id, course)
            
            if not prereq_ok:
                print(f"❌ Cannot register {course}. Missing prerequisites: {', '.join(missing_prereqs)}")
                continue
            
            if course not in registered_courses:
                registered_courses.append(course)
                # Get full course name for better feedback
                course_name = next((c for c in available_courses if c.startswith(course)), course)
                credits = course_credits.get(course, "N/A")
                print(f"✅ {course_name} (Credits: {credits}) registered successfully.")
            else:
                print(f"⚠️  {course} is already registered.")
        else:
            print("❌ Invalid Course ID. Please enter a valid course from the available list.")
            print(f"Available Course IDs: {', '.join(available_ids)}")
    
    return registered_courses

def display_registration_status(registered_courses, available_courses, student_id):
    """Display current registration status with financial information"""
    if registered_courses:
        print("\nYour registered courses are:")
        print("-" * 50)
        
        total_courses = len(registered_courses)
        total_credits, total_cost = calculate_tuition(registered_courses)
        
        for i, course_id in enumerate(registered_courses, 1):
            # Find the full course name
            course_name = next((c for c in available_courses if c.startswith(course_id)), course_id)
            credits = course_credits.get(course_id, "N/A")
            print(f"{i}. {course_name} (Credits: {credits})")
        
        print("-" * 50)
        print(f"📊 Registration Summary:")
        print(f"Total courses registered: {total_courses}")
        print(f"Total credit hours: {total_credits}")
        print(f"Estimated tuition: ${total_cost}")
        
        # Calculate potential GPA
        potential_gpa = calculate_potential_gpa(student_id, registered_courses)
        if potential_gpa != "N/A":
            print(f"Potential GPA after semester: {potential_gpa:.2f}")
        
        # Show remaining capacity (assuming max 15 credits per semester)
        max_credits = 15
        remaining_credits = max_credits - total_credits
        if remaining_credits > 0:
            print(f"You can register {remaining_credits} more credits.")
        elif remaining_credits == 0:
            print("You have reached the maximum credit limit for this semester.")
        else:
            print(f"⚠️  Credit overload: {abs(remaining_credits)} credits over limit!")
    else:
        print("No courses registered yet. Please register courses first.")

def save_registration(student_id, level, semester, registered_courses, available_courses):
    """Save registration to a file with detailed information"""
    filename = f"registration_{student_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        total_credits, total_cost = calculate_tuition(registered_courses)
        
        with open(filename, 'w') as file:
            file.write("=" * 50 + "\n")
            file.write("         COURSE REGISTRATION RECORD\n")
            file.write("=" * 50 + "\n")
            file.write(f"Student ID: {student_id}\n")
            file.write(f"Level: {level}\n")
            file.write(f"Semester: {semester}\n")
            file.write(f"Registration Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 50 + "\n")
            file.write("REGISTERED COURSES:\n")
            file.write("-" * 50 + "\n")
            
            for course_id in registered_courses:
                course_name = next((c for c in available_courses if c.startswith(course_id)), course_id)
                credits = course_credits.get(course_id, "N/A")
                file.write(f"- {course_name} (Credits: {credits})\n")
            
            file.write("-" * 50 + "\n")
            file.write(f"Total Courses: {len(registered_courses)}\n")
            file.write(f"Total Credits: {total_credits}\n")
            file.write(f"Estimated Tuition: ${total_cost}\n")
            file.write("=" * 50 + "\n")
        
        print(f"\n📄 Registration saved to {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving registration: {e}")
        return None

def registration_system(level, semester, student_id):
    """Main registration system loop"""
    available_courses = course_offerings.get((level, semester), [])
    registered_courses = []
    
    while True:
        print("\n" + "="*50)
        print("COURSE REGISTRATION SYSTEM")
        print("="*50)
        print("1. List available courses for the semester")
        print("2. Register Courses")
        print("3. Registration status")
        print("4. Calculate tuition")
        print("5. Save registration")
        print("6. Exit")
        print("="*50)

        try:
            choice = int(input("Select choice (1-6): "))
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1 and 6.")
            continue

        if choice == 1:
            display_courses(available_courses, student_id)

        elif choice == 2:
            registered_courses = register_courses(available_courses, registered_courses, student_id)

        elif choice == 3:
            display_registration_status(registered_courses, available_courses, student_id)

        elif choice == 4:
            if registered_courses:
                total_credits, total_cost = calculate_tuition(registered_courses)
                print(f"\n💰 Tuition Calculation:")
                print(f"Total Credits: {total_credits}")
                print(f"Estimated Tuition: ${total_cost}")
                print(f"Cost per credit: $50")
            else:
                print("❌ No courses registered yet.")

        elif choice == 5:
            if registered_courses:
                filename = save_registration(student_id, level, semester, registered_courses, available_courses)
                if filename:
                    print("✅ Registration successfully saved!")
            else:
                print("❌ No courses registered to save.")

        elif choice == 6:
            if registered_courses:
                save = input("Save registration before exiting? (y/n): ").lower()
                if save == 'y':
                    save_registration(student_id, level, semester, registered_courses, available_courses)
            print("\nExiting registration system. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please select a valid option (1-6).")

# Main program execution
if __name__ == "__main__":
    student_id, level, semester = get_student_info()
    
    if (level, semester) in course_offerings:
        print(f"\n✅ Successfully logged in as {student_id}, Level {level}, Semester {semester}")
        registration_system(level, semester, student_id)
    else:
        print(f"\n❌ No courses available for Level {level}, Semester {semester}")
        print("Please contact the administration office.")