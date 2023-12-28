from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('build_data.db')
    cursor = conn.cursor()

    # Fetch counts of successful and failed builds
    cursor.execute("SELECT build_status, COUNT(*) FROM builds GROUP BY build_status")
    counts = dict(cursor.fetchall())

    # Fetch build durations and timestamps for line chart
    cursor.execute("SELECT timestamp, duration FROM builds ORDER BY timestamp")
    build_durations = cursor.fetchall()
    build_timestamps = [entry[0] for entry in build_durations]
    build_durations = [entry[1] for entry in build_durations]

    # Fetch test results
    cursor.execute("SELECT tests_passed, tests_failed, timestamp FROM builds ORDER BY timestamp")
    test_data = cursor.fetchall()
    tests_passed = [entry[0] for entry in test_data]
    tests_failed = [entry[1] for entry in test_data]
    test_dates = [entry[2] for entry in test_data]

    conn.close()

    

    build_data = {
        'success': counts.get('Success', 0),
        'fail': counts.get('Failure', 0),
        'durations': build_durations,
        'timestamps': build_timestamps,
        'tests_passed': tests_passed,
        'tests_failed': tests_failed,
        'test_dates': test_dates
    }

    # Render the template and pass the build data to it
    return render_template('index.html', build_data=build_data)

if __name__ == '__main__':
    app.run(debug=True)
