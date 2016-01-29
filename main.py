import lattice
import person
import itertools

class Big:
    """This class will contain everything needed to run the simulation. It'll
    contain the lattice nodes, the various run functions, etc. All of my type
    annotations will be in Haskell style."""

    # Will be a tuple of 3d arrays, for swapping between the two, for memory
    # model efficiency. This will get initialized in init, just wanted to have
    # it here too for cleanliness.
    # ([[[Node]]],[[[Node]]])
    lattices = ([],[])

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
    def __init__(self,x_size,y_size,z_size):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

    # Just switches which lattice is being used. Will be called after every
    # time step.
    # Void -> Void
    def switch_lattice(self):
        self.cur_lattice = next_lattice()

    def next_lattice(self):
        return (self.cur_lattice + 1) % 2

    # Simulates for t timesteps. It'll draw and save a frame every draw_save
    # timesteps.
    # Int -> Int -> Void
    def Main(self,max_time_step,draw_save = 10000):
        for t in (0,max_time_step):
            step()
            if t % draw_save == 0:
                draw(int(self.y_size))
                save_drawing()

    # This function simply gets the neighbors of the Node node.
    # Node -> [Node]
    def get_neighbors(self,node):
        nodes = []
        for (a,b,c) in node.neighbor_indices:
            nodes += lattices[cur_lattice][a][b][c]
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
        for x in (0,self.x_size):
            for y in (0,self.y_size):
                for z in (0,self.z_size):
                    node = lattices[cur_lattice][x][y][z].copy()
                    neighbors = get_neighbors(node)
                    node.Update(neighbors)
                    lattices[next_lattice()][x][y][z] = node
        # This will pertubate all the temperatures of the nodes selected
        lattice[next_lattice()] = person.step(lattice[next_lattice()])
        switch_lattice()

    # This function will draw the data using matplotlib, plt.imshow() as used
    # the webpage
    # http://matplotlib.org/examples/pylab_examples/animation_demo.html
    # It will slice into the ndarray, pull out the temperatures, and then
    # display it.
    # Int -> Void
    # This slice will the slice from faucet side to the back of the individual
    # leaning against the far side of the tub.
    def draw(self, slice_ind):
        slice_node = GetSlice(slice_ind)
        # standard 2d python list of floats or whatever
        slice_temp = GetTemps(slice_node)
        p = plt.imshow(slice_temp)
        fig = plt.gcf()
        plt.clim()
        plt.title("Temperature of Bathtub")


b = Big(30,30,30)
