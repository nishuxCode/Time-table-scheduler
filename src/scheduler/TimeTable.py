from .Slot import Slot

class TimeTable:
    slot = []

    def __init__(self, data):
        TimeTable.slot = []
        days = data.days_per_week
        hours = data.hours_per_day
        
        # प्रति ग्रुप आवश्यक स्लॉट्स की संख्या (जैसे 6x6 = 36)
        slots_per_group = days * hours

        for sg in data.student_groups:
            count = 0
            # १. पहले असली विषयों के स्लॉट भरें
            for i in range(sg.nosubject):
                subject_name = sg.subject[i]
                teacher_name = sg.teacherid[i]
                total_hours = sg.hours[i]

                for _ in range(total_hours):
                    TimeTable.slot.append(Slot(sg, teacher_name, subject_name))
                    count += 1
            
            # २. बाकी बचे हुए घंटों को None (Free Period) से भरें
            # यह IndexError को रोकेगा
            while count < slots_per_group:
                TimeTable.slot.append(None)
                count += 1

    @staticmethod
    def return_slots():
        return TimeTable.slot
