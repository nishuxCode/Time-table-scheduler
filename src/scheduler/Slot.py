# src/scheduler/Slot.py

class Slot:
    def __init__(self, studentgroup=None, teacherid=None, subject=None):
        self.studentgroup = studentgroup
        self.teacherid = teacherid
        self.subject = subject

        # ✅ AUTO lab detection
        if subject is not None:
            name = subject.lower()
            self.is_lab = ("lab" in name) or ("project" in name)
        else:
            self.is_lab = False

    def __repr__(self):
        return f"{self.subject}"
