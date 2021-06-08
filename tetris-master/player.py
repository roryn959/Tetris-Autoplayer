from board import Direction, Rotation
from random import Random

class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
        ])

class RorysPlayer(Player):
    def __init__(self):
        from board import Shape
        self.revDict = {Shape.I:2, Shape.J:4, Shape.L:4, Shape.O:1, Shape.S:4, Shape.T:4, Shape.Z:2}
        self.a = -1
        self.b = -1
        self.c = -1
        self.d = 1
        
    def FindHeights(self, board):
        heights = [board.height for i in range(10)]
        for x in range(board.width):
            for y in range(board.height):
                if (x, y) in board.cells:
                    heights[x] = y
                    break
        return heights

    def FindHoles(self, board):
        holes = 0
        for (x, y) in board.cells:
            y += 1
            while y<24:
                if (x, y) in board.cells:
                    break
                else:
                    holes += 1
                y += 1
        return holes

    def FindDeviation(self, heights):
        total = 0
        for x in range(len(heights)-1):
            total += abs(heights[x]-heights[x+1])
        return total

    def FindScoreDiff(self, board, initial_score):
        return ((board.score-initial_score)//100)*100

    def ScoreBoard(self, board, initial_score):
        heights = self.FindHeights(board)

        #Find average height
        A = board.height-(sum(heights)/len(heights))

        #Find deviation of column height
        B = self.FindDeviation(heights)

        #Find number of holes
        C = self.FindHoles(board)

        #Find difference in board score
        D = board.score#self.FindScoreDiff(board.clone(), initial_score)
        
        return self.a*A+self.b*B+self.c*C+self.d*D

    def FindTarget(self, board, iteration=1):
        best_score = -10*6
        best_position = [0, 0, False] #Rotations, target_x, block landed
        if board.falling == None:
            print("Falling is none")
            return best_score, [0, 0, False]
        revs = self.revDict[board.falling.shape]        
        for r in range(revs):
            for x in range(9):
                newBoard = board.clone()
                landed = False
                initial_score = newBoard.score
                while newBoard.falling != None and newBoard.falling.left>x:
                    if newBoard.move(Direction.Left):
                        landed = True
                        break
                while newBoard.falling != None and newBoard.falling.left<x:
                    if newBoard.falling.right == board.width:
                        break
                    if newBoard.move(Direction.Right):
                        landed = True
                        break
                if not landed:
                    newBoard.move(Direction.Drop)
                if iteration == 1:
                    new_score, exPos = self.FindTarget(newBoard.clone(), 2)
                else:
                    new_score = self.ScoreBoard(newBoard, initial_score)
                if new_score>best_score:
                    best_score = new_score
                    best_position = [r, x, landed]
            if board.rotate(Rotation.Clockwise):
                break
        return best_score, best_position
    
    def choose_action(self, board):
        #print("Finding target...")
        predicted_score, target_position = self.FindTarget(board.clone())
        #print("Target:", predicted_score, target_position)
        action_list = []
        
        for r in range(target_position[0]):
            action_list.append(Rotation.Clockwise)
            board.rotate(Rotation.Clockwise)
            if board.falling == None:
                return Direction.Down

        if board.falling.left>target_position[1]:
            for x in range(board.falling.left-target_position[1]):
                action_list.append(Direction.Left)
        elif board.falling.left<target_position[1]:
            for x in range(target_position[1]-board.falling.left):
                action_list.append(Direction.Right)

        if not target_position[2]:
            action_list.append(Direction.Drop)
        
        return action_list

#SelectedPlayer = RandomPlayer
SelectedPlayer = RorysPlayer
