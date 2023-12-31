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

    tests_run = 15 # Fixed number of tests run 
    tests_failed = random.randint(0, 3)  # Reducing the range to lower fail probability
    tests_passed = tests_run - tests_failed

    # Simulate build steps with more realistic durations
    build_steps = [
        "Initializing build...",
        "Compiling source code...",
        "Linking libraries...",
        "Packaging assets...",
        "Finalizing build..."
    ]

    total_duration = 0
    for step in build_steps:
        # Duration between 5 and 30 minutes (represented in seconds)
        duration = random.uniform(300, 1800)
        total_duration += duration

    # New Logic: Randomize the number of changes and their types
    num_changes = random.randint(10, 15)
    change_types = ['Feature Addition', 'Bug Fix', 'Performance Improvement', 'Refactoring']
    team_skills = {'High': 0.05, 'Medium': 0.10, 'Low': 0.20}  # Failure probabilities

    build_failed = False
    fail_reason = ""
   # Dependency and environment factors
    dependency_failure_chance = 0.05  # 5% chance of failure due to dependency issues
    environment_failure_chance = 0.03  # 3% chance of failure due to environment issues

    # Check for random failure due to dependency or environment issues
    if random.random() < dependency_failure_chance:
        build_failed = True
        fail_reason = "Dependency failure"
    elif random.random() < environment_failure_chance:
        build_failed = True
        fail_reason = "Environment failure"

    for _ in range(num_changes):
        if build_failed:  # Skip processing changes if build already failed due to external factors
            break

        change_type = random.choice(change_types)
        is_critical = change_type in ["Compilation error", "Linker error"]  # Define critical change types
        team_skill = random.choice(list(team_skills.keys()))
        failure_probability = team_skills[team_skill]

        # Determine if the change fails
        if random.random() < failure_probability:
            build_failed = True
            fail_reason = f"{change_type} failed by {team_skill} skill team"
            if is_critical:
                break  # Critical failure causes immediate build failure

    # Set build status based on change failure
    build_status = "Fail" if build_failed else "Success"

    # Incorporate time of day and day of week logic
    time_of_day = random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])
    if time_of_day == 'Night':
        total_duration *= 0.8  # Assume 20% faster build times at night

    # Construct build information
    build_info = {
        'build_number': build_number,
        'day_of_week': current_day,
        'time_of_day': time_of_day,
        'duration': total_duration / 60,  # Convert duration to minutes
        'status': build_status,
        'tests_run': tests_run,
        'tests_passed': tests_passed,
        'tests_failed': tests_failed,
        'fail_reason': fail_reason if build_failed else None
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
