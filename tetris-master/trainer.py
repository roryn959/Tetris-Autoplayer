from repeated_runner import *
import numpy
import random

def sort(newList):
    n = len(newList)
    swapped = True
    while swapped:
        swapped = False
        for i in range(n-1):
            if newList[i]>newList[i+1]:
                x = newList[i]
                newList[i] = newList[i+1]
                newList[i+1] = x
                swapped = True
    return newList

class Trainer:
    def __init__(self):
        self.num_weights = 4
        self.num_variations = 50

        self.population = []

        for v in range(self.num_variations):
            new_weights = []
            for w in range(self.num_weights-1):
                new_weights.append(random.uniform(-2, 0))
            new_weights.append(random.uniform(0.8, 1.8))
            self.population.append(new_weights)
        self.show_pop()

    def show_pop(self):
        print("**********************")
        for g in self.population:
            print(f"\n***Gene {self.population.index(g)}***")
            for w in g:
                print(w)
        print("*********************\n")

    def test_gen(self, weights):
        scores = []
        for i in range(5, 8):
            score = run(i, weights)
            scores.append(score)
        return sort(scores)[1]

    def select(self, n):
        #print("Selecting from population", self.population)
        scores = []
        for i in range(self.num_variations):
            print("Testing gene", i)
            scores.append(self.test_gen(self.population[i]))
            print("Gene", i, "scored", scores[-1])
        #print("Evaluation:", scores)
        
        while len(scores)>n:
            lowest = [scores[0], 0]
            for i in range(len(scores)):
                if scores[i]<lowest[0]:
                    lowest = [scores[i], i]
            #print("Lowest:", lowest)
            del self.population[lowest[1]]
            del scores[lowest[1]]

        self.best = scores.index(max(scores))

        print("New population:")
        self.show_pop()
        print("\nBest weights found:", self.population[self.best], "with a score of", max(scores), "\n\n")

    def new_gen(self):
        new_population = []
        for i in range(self.num_variations):
            mother = self.population[random.randint(0, len(self.population)-1)]
            father = self.population[random.randint(0, len(self.population)-1)]
            child = []
            for w in range(self.num_weights):
                if random.randint(0, 1):
                    child.append(mother[w])
                else:
                    child.append(father[w])
            new_population.append(child)
        self.population = new_population

    def mutate(self, num_mutations):
        for n in range(num_mutations):
            p = random.randint(0, len(self.population)-1)
            w = random.randint(0, self.num_weights-1)
            c = random.uniform(-0.05, 0.05)
            self.population[p][w] += c

    def train(self, s, m):
        self.select(s)
        self.new_gen()
        self.mutate(m)

    def go(self, iterations, s, m):
        print("Initial population:")
        self.show_pop()
        for i in range(iterations):
            self.train(s, m)
            print("After", i, "runs:")
            self.show_pop()
            

t = Trainer()
default = [-0.5, -0.15403507007256478, -0.8, 0.6652842470923163]
t.population = [default]
t.new_gen()
t.mutate(100)
t.select(1)
