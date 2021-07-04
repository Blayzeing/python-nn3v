"""
The base shape class from which all shapes extend.

This class implements properties and systems common to all shapes, including
handling of a point list and transformation matrix, a colour selection system
allowing for the specification of a colour pallet, and a shading mode setting.

These properties can be choosen to be used or ignored by subclasses, with the
methods here acting more as a supporting framework and set of utilities to all
shape implementations.
"""
# TODO:
# Some abstract class here for generic objects; contains general properties:
#   -colour
#   -line colour
#   -mode (wire, points, solid)
#   -shading (smooth, solid)

class Shape
  def __init__(self, points):
  
