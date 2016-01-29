from lattice import Lattice
from math import sqrt
class Vector:
  """This class will hold a node's position in 3d space"""
  #Positions will be initialized in init
  x = 0  #Int
  y = 0  #Int
  z = 0  #Int

  #Initializes Vector with 3 floats representing an x,y,z position in 3d space
  #[Int, Int, Int] -> [Vector]
  def __init__(self, xx, yy,zz):
    self.x = xx
    self.y = yy
    self.z = zz

  #Returns string representing Vector
  #[Unit] -> [String]
  def __str__(self):
    return "<" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ">"




class Node(Lattice):
  """This class will represent either a air, body, or water lattice node"""

  #All will be initialized in init
  temp = 0.0                   #Float

  state = 0                    #Int
  #Air   will be represented as 0
  #Body  will be represented as 1
  #Water will be represented as 2
  #State is a psuedo Enum

  pos = Vector(0, 0, 0)  #Vector(Int, Int, Int)

  def __init__(self, t, s, xx, yy, zz):
    self.temp = t
    self.state = s
    self.pos = Vector(xx, yy, zz)

  #This will update the temperature of the node based on the time step and neighboring nodes
  #[[Node]] -> [Unit]
  def update(self, neighbors):
    temp += 1

  #Returns the state mapped to the appropiate string based on earlier documentation 
  #[Unit] -> [String]
  def get_state(self):
    if(self.state == 0):
      return "Air"
    elif(self.state == 1):
      return "Body"
    else:
      return "Water"  

  #Returns string version of Node
  def __str__(self):
    return "(" + str(self.temp) + "," + self.get_state() + "," + str(self.pos) + ")"

