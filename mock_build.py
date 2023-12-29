import sqlite3
import time
import random
import sys
import datetime

#DATABASE NEEDS TO BE UPDATED WITH NEW FIELDS!!!
def write_to_database(build_version, build_status, duration, tests_run, tests_passed, tests_failed, fail_reason):
    """
    Writes the build data to the SQLite database.
    """
    conn = sqlite3.connect('build_data.db')
    cursor = conn.cursor()
    
    # Insert the build data into the database
    cursor.execute("INSERT INTO builds (build_version, build_status, duration, tests_run, tests_passed, tests_failed, fail_reason) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (build_version, build_status, duration, tests_run, tests_passed, tests_failed, fail_reason))
    
    conn.commit()
    conn.close()

def get_next_day(current_day): 
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    next_day_index = (days.index(current_day)+1 % len(days))
    return days[next_day_index]

def generate_build(current_day, build_number):
    # Define the version for our mock build
    version = "1.0.1"
    print(f"Starting build for Project Alpha version {version}")
    # Simulate build steps
    build_steps = [
        "Initializing build...",
        "Compiling source code...",
        "Linking libraries...",
        "Packaging assets...",
        "Finalizing build..."
    ]

    total_duration = 0
    for step in build_steps:
        duration = random.uniform(0.5, 2.0)  # Random duration between 0.5 and 2 seconds
        total_duration += duration

    # Simulate build failure or success
    failure_chance = random.randint(1, 5)
    if failure_chance == 1:
        build_status = "Fail"
        error_messages = [
            "Compilation error in module XYZ",
            "Linker error: missing library ABC",
            "Asset not found: asset123.png",
            "Timeout error during build finalization",
            "Unknown error"
        ]
        fail_reason = random.choice(error_messages)
        tests_run, tests_passed, tests_failed = 0, 0, 0
    else:
        build_status = "Success"
        fail_reason = None
        # Simulate test results
        tests_run = random.randint(10, 20)
        tests_failed = random.randint(0, 5)
        tests_passed = tests_run - tests_failed

    # Incorporate time of day and day of week logic
    time_of_day = random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])
    if time_of_day == 'Night':
        total_duration *= 0.8  # Assume 20% faster build times at night

    build_info = {
        'build_number': build_number,
        'day_of_week': current_day,
        'time_of_day': time_of_day,
        'duration': total_duration,
        'status': build_status,
        'tests_run': tests_run,
        'tests_passed': tests_passed,
        'tests_failed': tests_failed,
        'fail_reason': fail_reason
    }

    return build_info, get_next_day(current_day)

    # Example usage
current_day = 'Monday'
build_number = 1
for _ in range(10):  # Generate 10 builds
    build_info, current_day = generate_build(current_day, build_number)
    print(build_info)
    build_number += 1

def main():
    current_day = 'Monday'
    build_number = 1

    for _ in range(100):  # Adjust the range as needed
        build_info, current_day = generate_build(current_day, build_number)
        write_to_database(build_info)
        build_number += 1

if __name__ == "__main__":
    main()
