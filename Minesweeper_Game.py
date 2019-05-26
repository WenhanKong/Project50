from __future__ import division
#import numpy as np
import random

def genFence(size,t):
    return '<DrawCuboid x1="0" y1="227" z1="0" x2="'+str(size+1)+'" y2="227" z2="'+str(size+1)+'" type="'+t+'"/>'

def genBlock(x,y,z,t):
    return '<DrawBlock x="'+str(x)+'" y="'+str(y)+'" z="'+str(z)+'" type="'+str(t)+'"/>'

def genBlockWithColor(x,y,z,t,c):
    return '<DrawBlock x="'+str(x)+'" y="'+str(y)+'" z="'+str(z)+'" type="'+str(t)+'" colour="'+str(c)+'"/>'

def genObservationFromGrid(size):
    return '<Grid name="board" absoluteCoords="1"> <min x="1" y="227" z="1"/> <max x="'+str(size)+'" y="228" z="'+str(size)+'10"/> </Grid>'

class Tile(object):
    def __init__(self):
        self.mine = False
        self.visible = False
        self.counter = 0

class Minesweeper(object):

    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.board = [[Tile() for n in range(size)] for n in range(size)]
        self.end = False 

        for i in range(num_mines):
            while True:
                x = random.randint(0,size-1)
                y = random.randint(0,size-1)
                if self.board[x][y].mine == False:
                    self.board[x][y].mine = True
                    break
        for row in range(self.size):
            for col in range(self.size):
                currentTile = self.board[row][col]
                if currentTile.mine == False:
                    for (dx, dy) in self.directions:
                        if self.inbounds(row+dx, col+dy)==True and self.board[row+dx][col+dy].mine == True:
                            self.board[row][col].counter+=1
    
    def drawBoard(self):
        res = ''
        #different color maps to counter in Tile Class.
        counter_color_dict = {1:'ORANGE', 2:'MAGENTA', 3:'LIGHT_BLUE', 4:'YELLOW', 5:'LIME', 6:'PINK', 7:'RED', 8:'BLACK'}
        
        #generate a diamond block fence with size of self.size * self.size
        res+=genFence(self.size, "diamond_block")
        for z in range(self.size):
            for x in range(len(self.board[z])):
                if self.board[x][z].mine == True:
                    res+=genBlock(x+1,227,z+1,"tnt")
                    res+="\n"
                else:
                    #tiles with no mines nearby are default wool
                    if self.board[x][z].counter == 0:
                        res+=genBlock(x+1,227,z+1,"wool")
                    else:
                        res+=genBlockWithColor(x+1, 227, z+1, "wool", counter_color_dict[self.board[x][z].counter])
                    res+="\n"
        #generate a snow layer as cover, not using genFence because layer starts at (1,1)
        res+='<DrawCuboid x1="1" y1="228" z1="1" x2="'+str(self.size)+'" y2="228" z2="'+str(self.size)+'" type="glass"/>'
        return res
    
    def play(self):
        self.printFullBoard()
        game_state = True
        while(game_state):
            game_state = self.sweep(int(input("Enter x:")), int(input("Enter y:")))
            self.printBoard()

    def sweep(self, row, col):
        if(self.board[row][col].mine):
            print('This Tile Is A Mine! You Lost!')
            self.end = True
            return False
        else:
            self.search(row, col)
            return True

    def search(self, row, col):
        #check if the coord is inbound
        if not self.inbounds(row, col):
            return
        #check if the tile is already visible or is it a mine
        tile = self.board[row][col]
        if tile.visible:
            return
        if tile.mine:
            return 
        #reveal a non mine non visible tile, stop if mines in adjacent tiles
        tile.visible = True
        if tile.counter > 0:
            return
        for (dx, dy) in self.directions:
            self.search(row+dx, col+dy)
        

    def inbounds(self, row, col):
        if 0<=row<self.size and 0<=col<self.size:
            return True
        else:
            return False

    def printBoard(self):
        res = []
        for row in self.board:
            temp = []
            for tile in row:
                if tile.visible == True:
                    temp.append(tile.counter)
                else:
                    temp.append("+")
            res.append(temp)
        for i in res:
            print(i)
    
    def printFullBoard(self):
        res = []
        for row in self.board:
            temp = []
            for tile in row:
                if tile.mine == True:
                    temp.append(9)
                else:
                    temp.append(tile.counter)
            res.append(temp)
        for i in res:
            print(i)



