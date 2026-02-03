from .data_models import StudentGroup, Teacher

class InputData:
    def __init__(self):
        self.student_groups = []
        self.teachers = []
        self.hours_per_day = 0
        self.days_per_week = 0
        self.break_slot = 3
        self.crossover_rate = 1.0
        self.mutation_rate = 0.1

    @property
    def no_student_group(self):
        return len(self.student_groups)

    @property
    def no_teacher(self):
        return len(self.teachers)

    def assign_teacher(self):
        """एक टीचर कई सब्जेक्ट पढ़ा सकता है (Comma separated support)"""
        for sg in self.student_groups:
            sg.teacherid = []  
            for subject_name in sg.subject:
                best_teacher_id = -1
                min_assigned = float('inf')
                s_sub = subject_name.lower().replace(" ", "")

                for i, teacher in enumerate(self.teachers):
                    # टीचर के सब्जेक्ट्स को कोमा से अलग करके चेक करें
                    t_subjects = [s.strip().lower().replace(" ", "") for s in teacher.subject.split(',')]
                    
                    match = False
                    if s_sub in t_subjects:
                        match = True
                    else:
                        for t_sub in t_subjects:
                            if t_sub and (t_sub in s_sub or s_sub in t_sub):
                                match = True
                                break

                    if match:
                        if teacher.assigned < min_assigned:
                            min_assigned = teacher.assigned
                            best_teacher_id = i
                
                if best_teacher_id != -1:
                    # Slot.py की जरूरत के अनुसार ID या Name भेजें (यहाँ Name भेजा है)
                    sg.teacherid.append(self.teachers[best_teacher_id].name)
                    self.teachers[best_teacher_id].assigned += 1
                else:
                    sg.teacherid.append("No Teacher") 
                    print(f"Warning: No teacher found for subject '{subject_name}' in group '{sg.name}'")

    def load_from_form(self, form):
        """Flask Form से डेटा लोड करने का पूरा वर्किंग कोड"""
        self.days_per_week = int(form.get("daysperweek", 5))
        self.hours_per_day = int(form.get("hoursperday", 7))
        self.break_slot = int(form.get("breakslot", 3))

        # १. पहले टीचर्स लोड करें (ताकि असाइनमेंट के लिए डेटा मौजूद हो)
        teacher_names = form.getlist("teacher")
        teacher_subjects = form.getlist("teachersubject")
        for i in range(len(teacher_names)):
            t = Teacher()
            t.id = i
            t.name = teacher_names[i].strip()
            t.subject = teacher_subjects[i].strip() # Example: "VLSI, Project"
            t.assigned = 0
            self.teachers.append(t)

        # २. स्टूडेंट ग्रुप्स लोड करें
        stgrp_names = form.getlist("studentgroup")
        stgrp_subjects = form.getlist("stgrpsubject")
        stgrp_hours = form.getlist("stgrphours")
        nosubjects = form.getlist("nosubject")
        
        sub_index = 0
        for i, name in enumerate(stgrp_names):
            sg = StudentGroup()
            sg.id = i
            sg.name = name
            num_subjects = int(nosubjects[i])
            sg.nosubject = num_subjects
            
            for _ in range(num_subjects):
                subj = stgrp_subjects[sub_index].strip()
                sg.subject.append(subj)
                
                # Hours Logic
                try:
                    h = int(stgrp_hours[sub_index])
                except:
                    h = 2 if "lab" in subj.lower() or "project" in subj.lower() else 1
                sg.hours.append(h)
                sub_index += 1
            
            self.student_groups.append(sg)

        # ३. अंत में टीचर असाइन करें
        self.assign_teacher()

    def load_from_file(self, filepath="c:/test/input.txt"):
        """फाइल से डेटा लोड करने का बेसिक स्ट्रक्चर (इसे अपनी फाइल के फॉर्मेट अनुसार बदलें)"""
        # फाइल लोडिंग का पुराना लॉजिक यहाँ रख सकते हैं, बस आखिर में self.assign_teacher() कॉल करें।
        pass
