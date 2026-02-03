from .TimeTable import TimeTable

class Utility:

    @staticmethod
    def print_input_data(data):
        print(
            "Nostgrp=", data.no_student_group,
            "Noteachers=", data.no_teacher,
            "daysperweek=", data.days_per_week,
            "hoursperday=", data.hours_per_day
        )

        for i in range(data.no_student_group):
            sg = data.student_groups[i]
            print(sg.id, sg.name)

            for j in range(sg.nosubject):
                print(
                    sg.subject[j],
                    sg.hours[j],
                    "hrs",
                    sg.teacherid[j]
                )
            print()

        for i in range(data.no_teacher):
            t = data.teachers[i]
            print(t.id, t.name, t.subject, t.assigned)

    @staticmethod
    def print_slots(data):
        days = data.days_per_week
        hours = data.hours_per_day
        nostgrp = data.no_student_group

        print("----Slots----")
        for i in range(days * hours * nostgrp):
            slot = TimeTable.slot[i]

            if slot is not None:
                print(
                    f"{i}- {slot.studentgroup.name} "
                    f"{slot.subject} {slot.teacherid}"
                )
            else:
                print("Free Period")

            if (i + 1) % (hours * days) == 0:
                print("******************************")
