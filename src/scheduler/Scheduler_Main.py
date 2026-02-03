import random
from .Chromosome import Chromosome
from .Gene import Gene
from .Utility import Utility
from .TimeTable import TimeTable


class SchedulerMain:
    final_chromosome = None

    def __init__(self, data):
        self.data = data
        self.populationsize = 1000
        self.maxgenerations = 100

        self.firstlist = []
        self.newlist = []

        # Print input data
        Utility.print_input_data(self.data)

        if self.data.no_student_group == 0:
            print("Error: No student groups provided. Skipping scheduling.")
            return

        # Generate slots
        TimeTable(self.data)

        # Print slots (testing)
        # Utility.print_slots() # Can be noisy, uncomment if needed

        # Initial population
        self.initialisePopulation()

        # Create new generations
        self.createNewGenerations()

    # ---------------- GENERATIONS ----------------

    def createNewGenerations(self):
        nogenerations = 0

        while nogenerations < self.maxgenerations:
            self.newlist = []

            # ELITISM (top 10%)
            for i in range(self.populationsize // 10):
                c = self.firstlist[i].deep_clone()
                self.newlist.append(c)

            i = self.populationsize // 10

            while i < self.populationsize:
                father = self.selectParentRoulette()
                mother = self.selectParentRoulette()

                # Crossover
                if random.random() < self.data.crossover_rate:
                    son = self.crossover(father, mother)
                else:
                    son = father

                # Mutation
                self.customMutation(son)

                if son.fitness == 1:
                    print("Selected Chromosome is:")
                    son.print_chromosome()
                    print("\nSuitable Timetable Generated\n")
                    son.print_timetable()
                    SchedulerMain.final_chromosome = son
                    return

                self.newlist.append(son)
                i += 1

            self.firstlist = self.newlist
            self.firstlist.sort()

            print(f"\n************** Generation {nogenerations + 2} **************\n")
            self.printGeneration(self.firstlist)

            nogenerations += 1

        if self.firstlist:
            print("Max generations reached. Returning best solution found.")
            best = self.firstlist[0]
            print(f"Best Chromosome Fitness: {best.fitness}")
            best.print_chromosome()
            best.print_timetable()
            SchedulerMain.final_chromosome = best

    # ---------------- SELECTION ----------------

    def selectParentRoulette(self):
        fitness_sum = sum(c.get_fitness() for c in self.firstlist[:self.populationsize // 10])
        pick = random.random() * fitness_sum
        current = 0

        for c in self.firstlist:
            current += c.get_fitness()
            if current >= pick:
                return c.deep_clone()

        return self.firstlist[0].deep_clone()

    # ---------------- MUTATION ----------------

    def customMutation(self, c):
        oldfitness = c.get_fitness()
        geneno = random.randint(0, self.data.no_student_group - 1)

        for _ in range(500000):
            c.gene[geneno] = Gene(geneno, self.data)
            if c.get_fitness() >= oldfitness:
                break

    # ---------------- CROSSOVER ----------------

    def crossover(self, father, mother):
        if self.data.no_student_group == 0:
            return father
            
        pos = random.randint(0, self.data.no_student_group - 1)

        temp = father.gene[pos].deep_clone()
        father.gene[pos] = mother.gene[pos].deep_clone()
        mother.gene[pos] = temp

        return father if father.get_fitness() > mother.get_fitness() else mother

    # ---------------- POPULATION ----------------

    def initialisePopulation(self):
        self.firstlist = []

        for _ in range(self.populationsize):
            c = Chromosome(self.data)
            self.firstlist.append(c)

        self.firstlist.sort()
        print("---------- Initial Generation ----------\n")
        self.printGeneration(self.firstlist)

    # ---------------- PRINTING ----------------

    def printGeneration(self, lst):
        print("Fetching details from this generation...\n")

        for i in range(4):
            print(f"Chromosome {i}: Fitness = {lst[i].get_fitness()}")
            lst[i].print_chromosome()
            print()

        print("Most fit chromosome fitness =", lst[0].get_fitness())
        print()

    # ---------------- MAIN ----------------


if __name__ == "__main__":
    SchedulerMain()
