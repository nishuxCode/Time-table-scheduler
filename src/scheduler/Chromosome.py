# chromosome.py

from .Gene import Gene
from .TimeTable import TimeTable

import copy

class Chromosome:
    def __init__(self, data):
        self.data = data
        self.fitness = 0.0
        self.point = 0
        self.gene = [Gene(i, self.data) for i in range(self.data.no_student_group)]
        self.fitness = self.get_fitness()

    def deep_clone(self):
        return copy.deepcopy(self)

    def get_fitness(self):
        self.point = 0
        hours = self.data.hours_per_day
        days = self.data.days_per_week
        nostgrp = self.data.no_student_group

        # 1. Teacher Collisions (Existing Logic)
        for i in range(hours * days):
            teacherlist = []
            for j in range(nostgrp):
                gene_j = self.gene[j]
                slot = None
                if TimeTable.slot[gene_j.slotno[i]] is not None:
                    slot = TimeTable.slot[gene_j.slotno[i]]

                if slot is not None:
                    # Check for None before accessing teacherid
                    if slot.teacherid is not None and slot.teacherid in teacherlist:
                        self.point += 1
                    else:
                        teacherlist.append(slot.teacherid)

        # 2. Consecutive Labs/Projects Penalty (New Logic)
        lab_penalty = 0
        for j in range(nostgrp):
            gene_j = self.gene[j]
            for d in range(days):
                # Get slots for the current day
                day_start_idx = d * hours
                daily_indices = gene_j.slotno[day_start_idx : day_start_idx + hours]
                
                for h in range(hours):
                    slot_idx = daily_indices[h]
                    current_slot = TimeTable.slot[slot_idx]
                    
                    if current_slot is not None:
                        subj = current_slot.subject.lower()
                        # If subject is Lab or Project, it should be adjacent to another slot of same subject
                        if "lab" in subj or "project" in subj:
                            is_connected = False
                            # Check previous slot in same day
                            if h > 0:
                                prev_idx = daily_indices[h-1]
                                prev_slot = TimeTable.slot[prev_idx]
                                if prev_slot is not None and prev_slot.subject == current_slot.subject:
                                    is_connected = True
                            # Check next slot in same day
                            if h < hours - 1:
                                next_idx = daily_indices[h+1]
                                next_slot = TimeTable.slot[next_idx]
                                if next_slot is not None and next_slot.subject == current_slot.subject:
                                    is_connected = True
                                    
                            if not is_connected:
                                lab_penalty += 1

        # Calculate Final Fitness
        total_penalty = self.point + lab_penalty
        # Use inverse relationship so fitness is always > 0 and higher is better
        self.fitness = 1.0 / (1.0 + total_penalty)
        
        return self.fitness

    def print_timetable(self):
        for i in range(self.data.no_student_group):
            # find first non-free slot to get batch name
            status = False
            l = 0
            while not status:
                if TimeTable.slot[self.gene[i].slotno[l]] is not None:
                    print(f"Batch {TimeTable.slot[self.gene[i].slotno[l]].studentgroup.name} Timetable-")
                    status = True
                l += 1

            # print timetable for each day
            for j in range(self.data.days_per_week):
                for k in range(self.data.hours_per_day):
                    slot_index = self.gene[i].slotno[k + j * self.data.hours_per_day]
                    slot = TimeTable.slot[slot_index]
                    if slot is not None:
                        print(slot.subject, end=" ")
                    else:
                        print("*FREE*", end=" ")
                print()
            print("\n\n")

    def print_chromosome(self):
        for i in range(self.data.no_student_group):
            print(" ".join(str(x) for x in self.gene[i].slotno))

    # for sorting chromosomes by fitness
    def __lt__(self, other):
        return self.fitness > other.fitness  # higher fitness is better
