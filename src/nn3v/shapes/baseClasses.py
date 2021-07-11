import math
import numpy as np
from traits.api import HasTraits, Array, Property, cached_property, List

# TODO:
# Some abstract class here for generic objects; contains general properties:
#   -colour
#   -line colour
#   -mode (wire, points, solid)
#   -shading (smooth, solid)

class TransformablePointCloud(HasTraits):
  """
  The base shape class from which all shapes extend.

  This class implements properties and systems common to all shapes, including
  handling of a point list and transformation matrix, a colour selection system
  allowing for the specification of a colour pallet, and a shading mode setting.

  These properties can be choosen to be used or ignored by subclasses, with the
  methods here acting more as a supporting framework and set of utilities to all
  shape implementations.
  """
  # The total pointcloud transform
  transform = Property(Array(shape=(4,4),value=np.eye(4)), depends_on=['positionMatrix','rotationMatrix','scaleMatrix'])

  # Scale array and it's associated cached matrix
  #scale = Array(shape=(3,), value=np.ones(3,))
  scale = List(value = [1,1,1])
  scaleMatrix = Property(Array(shape=(4,4), value=np.eye(4)), depends_on='scale')

  # Rotation array and it's associated cached matrix
  #rotation = Array(shape=(3,), value=np.zeros((3,)))
  rotation = List(value = [0,0,0])
  rotationMatrix = Property(Array(shape=(4,4), value=np.eye(4)), depends_on='rotation')

  # Position array and it's associated cached matrix
  #position = Array(shape=(3,), value=np.zeros((3,)))
  position = List(value = [0,0,0])
  positionMatrix = Property(Array(shape=(4,4), value=np.eye(4)), depends_on='position')
  
  @cached_property
  def _get_transform(self):
    print("Calculating transform...")
    return self.positionMatrix.dot(self.rotationMatrix).dot(self.scaleMatrix)

  @cached_property
  def _get_scaleMatrix(self):
    print("Calculating scale...")
    return( np.asarray([[self.scale[0],      0      ,      0      ,   0  ],
                        [     0       ,self.scale[1],      0      ,   0  ],
                        [     0       ,      0      ,self.scale[2],   0  ],
                        [     0       ,      0      ,      0      ,   1  ]]))

  @cached_property
  def _get_rotationMatrix(self):
    # Individual rotations
    print("Calculating rotation...")
    xRot = np.asarray([[             1             ,             0             ,              0            ,  0  ],
                       [             0             , math.cos(self.rotation[0]),-math.sin(self.rotation[0]),  0  ],
                       [             0             , math.sin(self.rotation[0]), math.cos(self.rotation[0]),  0  ],
                       [             0             ,             0             ,              0            ,  1  ]])
    yRot = np.asarray([[ math.cos(self.rotation[1]),             0             , math.sin(self.rotation[1]),  0  ],
                       [             0             ,             1             ,              0            ,  0  ],
                       [-math.sin(self.rotation[1]),             0             , math.cos(self.rotation[1]),  0  ],
                       [             0             ,             0             ,              0            ,  1  ]])
    zRot = np.asarray([[ math.cos(self.rotation[2]),-math.sin(self.rotation[2]),              0            ,  0  ],
                       [ math.sin(self.rotation[2]), math.cos(self.rotation[2]),              0            ,  0  ],
                       [             0             ,             0             ,              1            ,  0  ],
                       [             0             ,             0             ,              0            ,  1  ]])
    # Combine the rotations
    return yRot.dot(xRot).dot(zRot)
    
  @cached_property
  def _get_positionMatrix(self):
    print("Calculating translation...")
    translationMat = np.eye(4)
    translationMat[0:3,3] = self.position
    return translationMat
