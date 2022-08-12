import numpy as np

cornerA = np.array([300, 400])
cornerB = np.array([600, 350])
cornerC = np.array([580, 730])
cornerD = np.array([290, 700])


corners = [cornerA, cornerB, cornerC, cornerD]


def transform(corner_coordinates, target_width, target_height, input_coordinates):
    vectorAB = np.subtract(corner_coordinates[1], corner_coordinates[0])
    vectorBC = np.subtract(corner_coordinates[2], corner_coordinates[1])
    vectorCD = np.subtract(corner_coordinates[3], corner_coordinates[2])
    vectorDA = np.subtract(corner_coordinates[0], corner_coordinates[3])

    topIntersection = corner_coordinates[0] + \
                      vectorAB * ((input_coordinates[0] - corner_coordinates[0][0]) / vectorAB[0])
    rightIntersection = corner_coordinates[1] + \
                        vectorBC * ((input_coordinates[1] - corner_coordinates[1][1]) / vectorBC[1])
    bottomIntersection = corner_coordinates[2] + \
                        vectorCD * ((input_coordinates[0] - corner_coordinates[2][0]) / vectorCD[0])
    leftIntersection = corner_coordinates[3] + \
                         vectorDA * ((input_coordinates[1] - corner_coordinates[3][1]) / vectorDA[1])

    fraction_x = (input_coordinates[0] - leftIntersection[0]) / (rightIntersection[0] - leftIntersection[0])
    fraction_y = (input_coordinates[1] - topIntersection[1]) / (bottomIntersection[1] - topIntersection[1])

    target_coordinates = ([fraction_x * target_width, fraction_y * target_height])
    # print(fraction_x)
    # print(fraction_y)
    return target_coordinates

inputP = np.array([500, 500])
print(transform(corners, 1280, 720, inputP))
