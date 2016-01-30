import lattice
from node import Node
from node import Boundary
import person
import itertools
import matplotlib.pyplot as plt
import random

class Big:
    """This class will contain everything needed to run the simulation. It'll
    contain the lattice nodes, the various run functions, etc. All of my type
    annotations will be in Haskell style."""

    # Will be a tuple of 3d arrays, for swapping between the two, for memory
    # model efficiency. This will get initialized in init, just wanted to have
    # it here too for cleanliness.
    # ([[[Node]]],[[[Node]]])
    # This is technically a list cause apparently tuples are static.
    lattices = [[],[]]

    # The sizes will get initialized in init
    # Int
    x_size = 0
    y_size = 0
    z_size = 0

    # Int
    cur_lattice = 0




    # just sets the variables. Need to come up with an elegant way to describe
    #the shape of the tub, that will allow us to raise the amount of lattice
    #nodes
    def __init__(self,x_size,y_size,z_size,lattice):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.lattices[0] = lattice
        self.lattices[1] = lattice

    # Just switches which lattice is being used. Will be called after every
    # time step.
    # Void -> Void
    def switch_lattice(self):
        self.cur_lattice = self.next_lattice()

    def next_lattice(self):
        return (self.cur_lattice + 1) % 2

    # Simulates for t timesteps. It'll draw and save a frame every draw_save
    # timesteps.
    # Int -> Int -> Void
    def Main(self,max_time_step,draw_save = 10000):
        for t in range(0,max_time_step):
            self.step()
            if t % draw_save == 0:
                self.draw(int(self.x_size / 2.0))

                plt.savefig("first.png")

    # This function simply gets the neighbors of the Node node.
    # Node -> [Node]
    def get_neighbors(self,node):
        nodes = []
        for (a,b,c) in node.neighbor_indices:
            nodes.append(self.lattices[self.cur_lattice][a][b][c])
        return nodes

    # [Nodes] -> [Nodes]
    # TODO(aleeds) maybe do this last
    def UpdateBodyStatus(self,neighbors):
        # fill this in
        print "I am not a complete function yet!\n Do not use me\n\n\n"
        print "This was a message from UpdateBodyStatus"

    # This will step forward the sim by 1 timestep. I used 2 level indents to
    # me more room per line. This just runs throu

    def step(self):
        for x in range(0,self.x_size):
            for y in range(0,self.y_size):
                for z in range(0,self.z_size):
                    # may need to make copy function
                    node = self.lattices[self.cur_lattice][x][y][z]
                    if not node.isBoundary and node.state in [1,2]:

                      neighbors = self.get_neighbors(node)
                      node.update(neighbors)
                      self.lattices[self.next_lattice()][x][y][z] = node
        # This will pertubate all the temperatures of the nodes selected
        # self.lattices[self.next_lattice()] = person.step(self.lattices[self.next_lattice()])
        self.switch_lattice()


    def GetSlice(self,index):
        return self.lattices[self.cur_lattice][index]

    def GetTemps(self,nodes):
        temps = []
        for row in nodes:
            temp_row = []
            for node in row:
                if node.isBoundary:
                    temp_row.append(0)
                else:
                    temp_row.append(node.temp)
            temps.append(temp_row)
        return temps
    # This function will draw the data using matplotlib, plt.imshow() as used
    # the webpage
    # http://matplotlib.org/examples/pylab_examples/animation_demo.html
    # It will slice into the ndarray, pull out the temperatures, and then
    # display it.
    # Int -> Void
    # This slice will the slice from faucet side to the back of the individual
    # leaning against the far side of the tub.
    def draw(self, slice_ind):
        slice_node = self.GetSlice(slice_ind)
        # print slice_node
        # standard 2d python list of floats or whatever
        slice_temp = self.GetTemps(slice_node)
        print slice_temp
        p = plt.imshow(slice_temp)
        fig = plt.gcf()
        plt.clim()
        plt.title("Temperature of Bathtub")
        plt.show()



def_temp = 40

def volume_tub(x,y,z,volume_node):
    return x * y * z * volume_node

def BuildLatticeRectangularTub(x,y,z,volume_node):
    lattice = [[[0 for i in range(x)] for j in range(y)] for k in range(z)]
    wallx = [0,1,x - 2, x - 1]
    wally = [0,1,y - 2, y - 1]
    wallz = [z - 2, z - 1]
    for i in range(0,x):
        for j in range(0,y):
            for k in range(0,z):

                if i in wallx or j in wally or k in wallz:

                    lattice[i][j][k] = Boundary(i,j,k)
                elif k in [0,1]:
                    lattice[i][j][k] = Node(def_temp / 10,0,i,j,k,
                                            volume_node ** (2./ 3),
                                            volume_node,1)
                else:
                    lattice[i][j][k] = Node(def_temp + random.randrange(-20,20),
                                            2,i,j,k,
                                            volume_node ** (2./ 3),
                                            volume_node,1)


    return lattice


x = 10
y = 10
z = 10

b = Big(x,y,z,BuildLatticeRectangularTub(x,y,z,1))
b.Main(100)
