import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, render_template, session, send_from_directory
from scheduler.inputdata import InputData
from scheduler.Scheduler_Main import SchedulerMain
from scheduler.TimeTable import TimeTable

from front.User import User
app = Flask(__name__, template_folder='../../WebContent', static_folder='../../WebContent')

def prepare_view_data(scheduler):
    final_chromosome = scheduler.final_chromosome
    if final_chromosome is None:
        return [], 0, 0, [], []

    data = final_chromosome.data
    hours = data.hours_per_day
    days = data.days_per_week
    timetables = []

    break_after_index = getattr(data, 'break_slot', 3)

    for i in range(data.no_student_group):
        sg = data.student_groups[i]
        gene = final_chromosome.gene[i]

        weekly_slots = []
        for d in range(days):
            day_slots = []
            for h in range(hours):
                if h == break_after_index:
                    day_slots.append({"subject": "LUNCH", "teacher": "-"})

                slot_index = gene.slotno[d * hours + h]
                slot = TimeTable.slot[slot_index]

                if slot:
                    teacher_name = "Not Assigned"
                    if slot.teacherid:
                        for t in data.teachers:
                            if t.id == slot.teacherid:
                                teacher_name = t.name
                                break
                    day_slots.append({"subject": slot.subject, "teacher": teacher_name})
                else:
                    day_slots.append(None)

            weekly_slots.append(day_slots)

        timetables.append({"student_group": sg, "slots": weekly_slots})

    day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_names = day_labels[:days]

    time_slots = []
    current_hour = 9
    for i in range(hours):
        if i == break_after_index:
            time_slots.append("12:00 - 13:00 (LUNCH)")
            current_hour += 1
        
        time_slots.append(f"{current_hour}:00 - {current_hour+1}:00")
        current_hour += 1

    return timetables, hours, days, day_names, time_slots


# ---------- FROM FILE ----------
@app.route("/fromfile", methods=["GET"])
def from_file():
    # Create an instance of InputData and load from file
    data = InputData()
    data.load_from_file(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../input.txt')))

    # Run GA scheduler, passing the loaded data
    scheduler = SchedulerMain(data)

    timetables, hours, days, day_names, time_slots = prepare_view_data(scheduler)
    return render_template("view.html", timetables=timetables, hours=hours, days=days, day_names=day_names, time_slots=time_slots)

@app.route("/view-timetable", methods=["GET"])
def view_timetable():
    return from_file()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User(username=username, password=password)
    login_result = user.login()

    if login_result == "success":
        return render_template('index.html')
    else:
        return render_template('login-error.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    country = request.form['country']

    user = User(username=username, password=password, email=email, country=country)
    register_result = user.register()

    if register_result == "success":
        return render_template('register-success.html')
    else:
        return render_template('register-error.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/how-to-use')
def how_to_use():
    return render_template('how-to-use.html')

@app.route('/contact', methods=['POST'])
def contact():
    return "Message received", 200

@app.route('/readme-images/<path:filename>')
def serve_readme_images(filename):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    return send_from_directory(os.path.join(root_dir, 'readme-images'), filename)

# AJAX Routes for form dynamic fields
@app.route('/showteachers')
def show_teachers():
    val = request.args.get('val')
    return render_template('showteachers.html', val=int(val) if val else 0)

@app.route('/showstgrp')
def show_stgrp():
    val = request.args.get('val')
    return render_template('showstgrp.html', val=int(val) if val else 0)

@app.route('/showhours')
def show_hours():
    val = request.args.get('val')
    return render_template('showhours.html', val=int(val) if val else 0)

@app.route('/showstgrpsubject')
def show_stgrpsubject():
    val = request.args.get('val')
    return render_template('showstgrpsubject.html', val=int(val) if val else 0)

@app.route('/showdays')
def show_days():
    val = request.args.get('val')
    return render_template('showdays.html', val=int(val) if val else 0)

@app.route('/')
def login_page(): return render_template('login.html')

# ---------- FROM FORM ----------
@app.route("/fromform", methods=["POST"])
def from_form():
    # Create an instance of InputData and load from the form
    data = InputData()
    data.load_from_form(request.form)

    # Run scheduler with the form data
    scheduler = SchedulerMain(data)
    timetables, hours, days, day_names, time_slots = prepare_view_data(scheduler)
    return render_template("view.html", timetables=timetables, hours=hours, days=days, day_names=day_names, time_slots=time_slots)


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
