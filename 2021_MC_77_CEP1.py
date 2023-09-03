# Registratioin Number : 2021-MC-77
# Name : Muhammad Faisal
# Section : B
# Home Work : CEP - 1
# Date : 5th March 2023
# Submitted To : Sir Doctor Muhammad Ahsan Naeem

import random
from copy import deepcopy
from pyamaze import maze, agent

rows = 6
columns = 6
population = []
populationSize = 500
FinalObstacles = []
FinalTurns = []
FinalSteps = []
FinalFitness = []
dictionary = {}

# Create the maze and agent
m = maze(rows, columns)
m.CreateMaze(loopPercent=100)
a = agent(m, filled=True, footprints=True, shape="arrow")
mazeMap = m.maze_map

def initialPopulation():
    pop = []
    if rows <= columns:
        for i in range(populationSize):
            pop.append(1)
            for j in range(columns-2):
                pop.append(random.randint(1, rows)) # Vertical Movement of agent in maze
            pop.append(rows)
            population.append(pop)
            pop = []
    else:
        for i in range(populationSize):
            pop.append(1)
            for j in range(rows-2):
                pop.append(random.randint(1, columns)) # Horizontal Movement of agent in maze
            pop.append(columns)
            population.append(pop)
            pop = []

def mutation():
    if rows <= columns:
        for i in population:
            i[random.randint(1, columns-2)] = random.randint(1, rows)
    else:
        for i in population:
            i[random.randint(1, rows-2)] = random.randint(1, columns)

def crossover():
    for i in range(0, populationSize//2, 2):
        parent1 = deepcopy(population[i])
        parent2 = deepcopy(population[i+1])

        if rows <= columns:
            for j in range(random.randint(1, columns-2), columns):
                parent1[j], parent2[j] = parent2[j], parent1[j]
        else:
            for j in range(random.randint(1, rows-2), rows):
                parent1[j], parent2[j] = parent2[j], parent1[j]

        population[(populationSize//2)+i] = parent1
        population[(populationSize//2)+(i+1)] = parent2

noOfTurns = []
path = []
obstacles = []
noOfSteps = []
def Fitness():
# Finding Path
    p = []
    for i in population:
        if rows <= columns:
            for j in range(columns-1):
                if (i[j+1]-i[j]) >= 0:
                    for k in range(i[j], i[j+1]+1):
                        p.append((k, j+1))
                if (i[j+1]-i[j]) < 0:
                    for k in range(i[j], i[j+1]-1, -1):
                        p.append((k, j+1))
            p.append((rows, columns))
        else:
            for j in range(rows-1):
                if (i[j+1]-i[j]) >= 0:
                    for k in range(i[j], i[j+1]+1):
                        p.append((j+1, k))
                if (i[j+1]-i[j]) < 0:
                    for k in range(i[j], i[j+1]-1, -1):
                        p.append((j+1, k))
            p.append((rows, columns))
        path.append(p)
        p = []

# Obstacles
    obs = 0
    for i in path:
        for j in range(len(i) - 1):
            if i[j+1][0]-i[j][0] >= 0 and i[j+1][1] == i[j][1]:
                if mazeMap[(i[j])]["S"] == 0:
                    obs += 1
            if i[j+1][0]-i[j][0] < 0 and i[j+1][1] == i[j][1]:
                if mazeMap[(i[j])]["N"] == 0:
                    obs += 1
            if i[j+1][1]-i[j][1] >= 0 and i[j+1][0] == i[j][0]:
                if mazeMap[(i[j])]["E"] == 0:
                    obs += 1
            if i[j+1][1]-i[j][1] < 0 and i[j+1][0] == i[j][0]:
                if mazeMap[(i[j])]["W"] == 0:
                    obs += 1
        obstacles.append(obs)
        obs = 0

# Number of steps
    for i in path:
        noOfSteps.append(len(i))

# Number of turns
    turns = 0
    for i in population:
        for j in range(len(i) - 1):
            if i[j + 1] != i[j]:
                turns += 1
        noOfTurns.append(turns+1)
        turns = 0

# Fitness Value using Formulas
    minimumObstacles = min(obstacles)
    maximumObstacles = max(obstacles)
    minimumTurns = min(noOfTurns)
    maximumTurns = max(noOfTurns)
    minimumSteps = min(noOfSteps)
    maximumSteps = max(noOfSteps)
    weightOfObstacle = 3
    weightOfPath = 2
    weightOfTurn = 3

    for i in range(populationSize):
        finalObstacles = (1 - ((obstacles[i] - minimumObstacles) / (maximumObstacles - minimumObstacles)))
        FinalObstacles.append(finalObstacles)
        finalTurns = (1 - ((noOfTurns[i] - minimumTurns) / (maximumTurns - minimumTurns)))
        FinalTurns.append(finalTurns)
        finalSteps = (1 - ((noOfSteps[i] - minimumSteps) / (maximumSteps - minimumSteps)))
        FinalSteps.append(finalSteps)
        finalFitness = ((100 * weightOfObstacle * FinalObstacles[i]) * ( ((weightOfPath * FinalSteps[i]) + (weightOfTurn * FinalTurns[i])) / (weightOfPath + weightOfTurn)))
        FinalFitness.append(finalFitness)

# Bubble sorting in descending order
def sorting():
    for i in range(populationSize - 1):
        for j in range(i+1, populationSize):
            if FinalFitness[j] > FinalFitness[i]:
                FinalFitness[j], FinalFitness[i] = FinalFitness[i], FinalFitness[j]
                population[j], population[i] = population[i], population[j]
    for i in range(populationSize):
        print(f"{population[i]}          {FinalFitness[i]}")

def solution():
    sol = []
    for i in range(populationSize):
        if FinalFitness[i] >= 0 and obstacles[i] == 0:
            sol = path[i]
            for j in range(len(sol) - 1):
                dictionary.update({sol[j+1]:sol[j]}) # This loop updates a dictionary named dictionary where the keys represent the coordinates of the cells that form the path, and the values represent the coordinates of the cells that should be visited next in order to follow the path.
            return 1
    return 0

# Main Function
initialPopulation()
i = 0
while True:
    i+=1
    Fitness()
    if solution():
        print(f"Solution found in iteration number = {i}")
        m.tracePath({a:dictionary})
        m.run()
        break
    sorting()
    crossover()
    mutation()