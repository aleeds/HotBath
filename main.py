# TODO Mixing by the person, by time/bath condition/etc
# TODO begin experimenting with the various conditions, making sure it matches
#      real life.
# TODO the paper, the actual modelling.


import lattice
from node import Node
from node import Boundary
import person
import itertools
import matplotlib.pyplot as plt
import random
from math import sqrt

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
        self.faucet_x = self.x_size / 2
        self.faucet_y = 2
        self.faucet_width = 1
        self.faucet_length = 1
        self.faucet_temp = 74
        self.faucet_node_depth = 4 #z_size - 3

    # Just switches which lattice is being used. Will be called after every
    # time step.
    # Void -> Void
    def switch_lattice(self):
        self.cur_lattice = self.next_lattice()

    def next_lattice(self):
        return (self.cur_lattice + 1) % 2


    def faucet(self, x, y, length, width, node_depth, temp):
      for d in range(0, node_depth):
        for xx in range(max(width-x, 0), width+x):  #might be negative
          for yy in range(max(y-width, 0), y+width):  #might be negative
            self.lattices[self.cur_lattice][xx][yy][d].temp = temp




    # Swap out how it mixes whenever we want to
    def MixingFrequency(self,t,freq):
        if (t - 1) % freq == 0:
            MixingOne(self.lattices[self.cur_lattice])

    # Simulates for t timesteps. It'll draw and save a frame every draw_save
    # timesteps.
    # Int -> Int -> Void
    def Main(self, max_time_step, draw_save = 10000):
        for t in range(0,max_time_step):
            if t % 10 == 0:
                print t
            self.step()
            self.MixingFrequency(t, 2000)
            self.switch_lattice()
            if t % draw_save == 0:
                self.draw(int(self.x_size / 2.0),t)
                self.draw(4,t)
                #self.draw(10)

                ##plt.savefig("first.png")
                self.TempStatistics()
                plt.show()


    # This function simply gets the neighbors of the Node node.
    # Node -> [Node]
    def get_neighbors(self,node):
        nodes = []
        if(not node.isBody):
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
        self.faucet(self.faucet_x, self.faucet_y,
                    self.faucet_length,
                    self.faucet_width,
                    self.faucet_node_depth,
                    self.faucet_temp)

        for x in range(0,self.x_size):
            for y in range(0,self.y_size):
                for z in range(0,self.z_size):
                    # may need to make copy function
                    node = self.lattices[self.cur_lattice][x][y][z]
                    if not node.isBoundary and node.state in [1,2]:

                      neighbors = self.get_neighbors(node)
                      node.update(neighbors)
                      self.lattices[self.next_lattice()][x][y][z] = node
                      #set body nodes to initial temp

        # This will pertubate all the temperatures of the nodes selected
        # self.lattices[self.next_lattice()] = person.step(self.lattices[self.next_lattice()])
        self.faucet(self.faucet_x, self.faucet_y,
                    self.faucet_length,
                    self.faucet_width,
                    self.faucet_node_depth,
                    self.faucet_temp)



    def GetSlice(self,index):
      ret = []
    #   for i in range(0,self.x_size):
    #     tmp = []
    #     for j in range(0,self.y_size):
    #       if j == index:
    #         for k in range(0,self.z_size):
    #           tmp.append(self.lattices[self.cur_lattice][i][j][k])
    #     ret.append(tmp)

      return self.lattices[self.cur_lattice][index]

    def GetTemps(self,nodes):
        temps = []
        for row in nodes:
            temp_row = []
            for node in row:
                if node.isIndicator:
                    temp_row.append(100)
                else:
                    temp_row.append(node.temp)
            temps.append(temp_row)
        temps = zip(*temps[::-1])
        return temps

    def TempStatistics(self):
        temps = []
        for plane in self.lattices[self.cur_lattice]:
            for row in plane:
                for node in row:
                    if not node.isBoundary and node.state == 2 and node.temp != self.faucet_temp:
                        temps.append(node.temp)
        mean = sum(temps)/len(temps)
        temps_minus_mean_squared = [(temp - mean) ** 2 for temp in temps]
        std_dev = sqrt(sum(temps_minus_mean_squared)/len(temps_minus_mean_squared))
        plt.hist(temps)
        plt.xlabel("Temp")
        plt.ylabel("Counts")
        plt.title("Mean: " + str(mean) + " std_dev: " + str(std_dev))
    # This function will draw the data using matplotlib, plt.imshow() as used
    # the webpage
    # http://matplotlib.org/examples/pylab_examples/animation_demo.html
    # It will slice into the ndarray, pull out the temperatures, and then
    # display it.
    # Int -> Void
    # This slice will the slice from faucet side to the back of the individual
    # leaning against the far side of the tub.
    def draw(self, slice_ind, t):
        plt.clf()
        slice_node = self.GetSlice(slice_ind)
        # print slice_node
        # standard 2d python list of floats or whatever
        slice_temp = self.GetTemps(slice_node)
        #slice_temp = [[int(i) for i in row] for row in slice_temp]

        #print slice_temp
        p = plt.imshow(slice_temp,cmap = "bwr")
        plt.colorbar()
        fig = plt.gcf()
        plt.clim()
        plt.title("Temperature of Bathtub (time_step:" + str(t) + ")\n") 
        plt.plot([-2,self.y_size], [1,1], '-k')
        plt.show()



def_temp = 50
room_temp = 21

def volume_tub(x,y,z,volume_node):
    return x * y * z * volume_node

def BuildLatticeRectangularTub(x,y,z,volume_node,body):
    lattice = [[[0 for i in range(z)] for j in range(y)] for k in range(x)]
    wallx = [0, 1, x - 2, x - 1]
    wally = [0, 1, y - 2, y - 1]
    wallz = [z - 2, z - 1]

    for i in range(0,x):
        for j in range(0,y):
            for k in range(0,z):
                if (i,j,k) in body:
                    lattice[i][j][k] = Node(37,
                                            1,i,j,k,
                                            volume_node ** (2./ 3),
                                            volume_node,1) # this is the size of skin, was 4
                elif i in wallx or j in wally or k in wallz:
                    lattice[i][j][k] = Boundary(i,j,k)
                    if j == 0:
                        lattice[i][j][k].isIndicator = True

                elif k in [0,1]:
                    lattice[i][j][k] = Node(room_temp,0,i,j,k,
                                            volume_node ** (2./ 3),
                                            volume_node,1)
                else:
                    lattice[i][j][k] = Node(def_temp + random.randrange(-1,1),
                                            2,i,j,k,
                                            volume_node ** (2./ 3),
                                            volume_node,1)


    return lattice

# (Int, Int, Int, Int, Int, Int) -> [(Int,Int,Int)]
def make_body(body_x, body_y, body_z, x_width, y_length, z_height):
  body = [(i,j,k) for i in range(body_x - x_width, body_x + x_width)
                  for j in range(body_y - y_length, body_y + y_length)
                  for k in range(body_z - z_height, body_z + z_height)]


  temp = [(i,j,k) for i in range(body_x, body_x + x_width)
                  for j in range(body_y, body_y + y_length)
                  for k in range(0, body_z)]

  body += temp
  return body

def GetRandomWater(lattice):
    node = lattice[0][0][0]
    while node.isBoundary or node.state != 2:
        i = random.randrange(0,len(lattice))
        j = random.randrange(0,len(lattice[0]))
        k = random.randrange(0,len(lattice[0][0]))
        node = lattice[i][j][k]
    return node

# This mixing function will take in the current lattice, and swap all the
# temperatures of all the water in the tub randomly. This will simulate the
# person thrashing in the tub
def MixingOne(lattice):
    for plane in lattice:
        for line in plane:
            for node in line:
                if not node.isBoundary and node.state == 2:
                    node.temp = GetRandomWater(lattice).temp

# This mixing function will move the temperatures of water close to the faucet
# to temperatures close to the body, and vice versa. This will simulate a
# lateral movement from the front to the back
def MixingTwo(lattice,lens):
    y_size = len(lattice[0])
    for plane in lattice:
        for line in plane:
            for node in line:
                if not node.isBoundary and node.state == 2:
                    pos = node.pos
                    node.temp = lattice[pos.x][(pos.y + lens) % y_size ][pos.z].temp


x = int(32./3)
y = int(48./3)
z = int(25./3)

body_pos_x = x/2
body_pos_y = int(y*4./5)
body_pos_z = int(z*2./3)

body_width = x/4   # x
body_length = y/6  # y
body_height = z/6  # z

body = make_body(body_pos_x, body_pos_y, body_pos_z, body_width, body_length, body_height)



b = Big(x,y,z,BuildLatticeRectangularTub(x,y,z,1,body))
b.Main(1100,100)
