import os
import sys

# Add src to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from front.Timetable_Action import app

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)