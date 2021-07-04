"""
The base shape class from which all shapes extend.

This class implements properties and systems common to all shapes, including
handling of a point list and transformation matrix, a colour selection system
allowing for the specification of a colour pallet, and a shading mode setting.

These properties can be choosen to be used or ignored by subclasses, with the
methods here acting more as a supporting framework and set of utilities to all
shape implementations.
"""

import numpy as np
from traits.api import HasTraits, Array

# TODO:
# Some abstract class here for generic objects; contains general properties:
#   -colour
#   -line colour
#   -mode (wire, points, solid)
#   -shading (smooth, solid)

class Shape(HasTraits):
  #transform = Property(Array(shape=(4,4),value=np.eye(4)), depends_on=['position','rotation'])
  transform = Array(shape=(4,4),value=np.eye(4))
  position = Property(Array(shape=(3,)), depends_on='transform')
  rotation = Property(Array(shape=(3,)), depends_on='transform')
  scale = Property(Float, depends_on='transform')

  def _get_position(self):
    # 
  
