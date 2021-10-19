import math
import numpy as np
from traits.api import HasTraits, Array, Property, cached_property, List, Float, TraitType, Disallow, Event

# TODO:
# Some abstract class here for generic objects; contains general properties:
#   -colour
#   -line colour
#   -mode (wire, points, solid)
#   -shading (smooth, solid)

class Vector3(HasTraits):
  """
  A simple class for vector operations.
  """
  ## The three dimensions
  x = Float(value=0.0)
  y = Float(value=0.0)
  z = Float(value=0.0)
  updated = Event

  def __init__(self, xVal=0, yVal=0, zVal=0):
    super().__init__()
    self.x = xVal
    self.y = yVal
    self.z = zVal

  def somethingHasHappened(self):
    self.updated = True

#class TransformablePointCloud(HasTraits):
#  """
#  The base shape class from which all shapes extend.
#
#  This class implements properties and systems common to all shapes, including
#  handling of a point list and transformation matrix, a colour selection system
#  allowing for the specification of a colour pallet, and a shading mode setting.
#
#  These properties can be choosen to be used or ignored by subclasses, with the
#  methods here acting more as a supporting framework and set of utilities to all
#  shape implementations.
#  """
#  
#  # The point list for this object
#  points = List(value=[])
#  worldPoints = Property(Array(shape=(4,)), depends_on="points")

class TransformFrame(HasTraits):

  # Scale array and it's associated cached matrix
  scale = Vector3(1.0, 1.0, 1.0)
  scaleMatrix = Property(Array(shape=(4,4), value=np.eye(4)), depends_on='scale:[x,y,z]')

  # Rotation array and it's associated cached matrix
  rotation = Vector3(0.0, 0.0, 0.0)
  rotationMatrix = Property(Array(shape=(4,4), value=np.eye(4)), depends_on='rotation:[x,y,z]')

  # Position array and it's associated cached matrix
  position = Vector3(0.0, 0.0, 0.0)
  positionMatrix = Property(Array(shape=(4,4), value=np.eye(4)), depends_on='position:[x,y,z]')

  # The total pointcloud transform
  transform = Property(Array(shape=(4,4),value=np.eye(4)), depends_on=['positionMatrix','rotationMatrix','scaleMatrix'])
  
  @cached_property
  def _get_transform(self):
    print("Calculating transform...")
    return self.positionMatrix.dot(self.rotationMatrix).dot(self.scaleMatrix)

  @cached_property
  def _get_scaleMatrix(self):
    print("Calculating scale matrix...")
    return( np.asarray([[self.scale.x ,      0      ,      0      ,   0  ],
                        [     0       ,self.scale.y ,      0      ,   0  ],
                        [     0       ,      0      ,self.scale.z ,   0  ],
                        [     0       ,      0      ,      0      ,   1  ]]))

  @cached_property
  def _get_rotationMatrix(self):
    # Individual rotations
    print("Calculating rotation matrix...")
    xRot = np.asarray([[             1             ,             0             ,              0            ,  0  ],
                       [             0             , math.cos(self.rotation.x) ,-math.sin(self.rotation.x) ,  0  ],
                       [             0             , math.sin(self.rotation.x) , math.cos(self.rotation.x) ,  0  ],
                       [             0             ,             0             ,              0            ,  1  ]])
    yRot = np.asarray([[ math.cos(self.rotation.y) ,             0             , math.sin(self.rotation.y) ,  0  ],
                       [             0             ,             1             ,              0            ,  0  ],
                       [-math.sin(self.rotation.y) ,             0             , math.cos(self.rotation.y) ,  0  ],
                       [             0             ,             0             ,              0            ,  1  ]])
    zRot = np.asarray([[ math.cos(self.rotation.z) ,-math.sin(self.rotation.z) ,              0            ,  0  ],
                       [ math.sin(self.rotation.z) , math.cos(self.rotation.z) ,              0            ,  0  ],
                       [             0             ,             0             ,              1            ,  0  ],
                       [             0             ,             0             ,              0            ,  1  ]])
    # Combine the rotations
    return yRot.dot(xRot).dot(zRot)
    
  @cached_property
  def _get_positionMatrix(self):
    print("Calculating translation matrix...")
    translationMat = np.eye(4)
    translationMat[0:3,3] = [self.position.x, self.position.y, self.position.z]
    return translationMat
