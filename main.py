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
                draw()
                save_drawing()

    # This function simply gets the neighbors of the Node node.
    # Node -> [Node]
    def get_neighbors(self,node):
        # fill this in.
        print "I am not a complete function yet!\n Do not use me\n\n\n"
        print "This was a message from get_neighbors"

    # [Nodes] -> [Nodes]
    def UpdateBodyStatus(self,neighbors):
        # fill this in
        print "I am not a complete function yet!\n Do not use me\n\n\n"
        print "This was a message from UpdateBodyStatus"

    # This will step forward the sim by 1 timestep. I used 2 level indents to
    # me more room per line.
    def step(self):
        for x in (0,x_size):
            for y in (0,y_size):
                for z in (0,z_size):
                    node = lattices[cur_lattice][x][y][z].copy()
                    neighbors = UpdateBodyStatus(get_neighbors(node))
                    node.Update(neighbors)
                    lattices[next_lattice()][x][y][z] = node
        person.step()
