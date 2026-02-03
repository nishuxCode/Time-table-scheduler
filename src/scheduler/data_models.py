class StudentGroup:
    """A class to hold data for a student group."""
    def __init__(self):
        self.id = 0
        self.name = ""
        self.nosubject = 0
        self.subject = []
        self.hours = []
        self.teacherid = [] 
        self.is_lab = []  # Teacher ID for each subject

    def __repr__(self):
        return f"StudentGroup(name={self.name})"

class Teacher:
    """A class to hold data for a teacher."""
    def __init__(self):
        self.id = 0
        self.name = ""
        self.subject = ""
        self.assigned = 0  # Number of groups assigned to this teacher

    def __repr__(self):
        return f"Teacher(name={self.name})"