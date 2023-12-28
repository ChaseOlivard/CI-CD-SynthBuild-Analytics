import sqlite3
import time
import random
import sys

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


def main():
    # Define the version for our mock build
    version = "1.0.0"
    print(f"Starting build for Project Alpha version {version}")

    build_steps = [
        "Initializing build...",
        "Compiling source code...",
        "Linking libraries...",
        "Packaging assets...",
        "Finalizing build..."
    ]

    total_duration = 0
    for step in build_steps:
        print(step)
        duration = random.uniform(0.5, 2.0)  # Random duration between 0.5 and 2 seconds
        time.sleep(duration)
        total_duration += duration

    failure_chance = random.randint(1, 5)
    if failure_chance == 1:
        # Simulate a failure
        print("Build failed!")
        error_messages = [
            "Compilation error in module XYZ",
            "Linker error: missing library ABC",
            "Asset not found: asset123.png",
            "Timeout error during build finalization",
            "Unknown error"
        ]
        error_msg = random.choice(error_messages)
        print(f"Error: {error_msg}")
        write_to_database(version, "Fail", total_duration, 0, 0, 0, error_msg)
        sys.exit(1)
    else:
        print(f"Build completed successfully for Project Alpha version {version} in {total_duration:.2f} seconds")
        # Simulate test results
        tests_run = random.randint(10, 20)
        tests_failed = random.randint(0, 5)
        tests_passed = tests_run - tests_failed
        write_to_database(version, "Success", total_duration, tests_run, tests_passed, tests_failed, None)

if __name__ == "__main__":
    main()
