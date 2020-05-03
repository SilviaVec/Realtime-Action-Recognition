
import numpy as np
import matplotlib.pyplot as plt
import math


def get_joint(x, idx):                                                #MODIFIED
    px = x[3*idx]
    py = x[3*idx+1]
    pz = x[3*idx+2]
    return px, py, pz

 
def set_joint(x, idx, px, py, pz):                                    #MODIFIED
    x[3*idx] = px
    x[3*idx+1] = py
    x[3*idx+2] = py
    return


def get_an_example_of_standing_skeleton():                           #TODO
    data = [7, 67, 7041, "stand", "stand_03-08-20-24-55-587/00055.jpg", 0.5670731707317073, 0.11005434782608697, 0.5670731707317073, 0.18342391304347827, 0.5182926829268293, 0.1875, 0.5030487804878049, 0.27309782608695654, 0.5030487804878049, 0.34239130434782605, 0.6189024390243902, 0.18342391304347827, 0.6310975609756098, 0.2649456521739131, 0.6310975609756098, 0.3342391304347826, 0.5365853658536586,
            0.34646739130434784, 0.5335365853658537, 0.46467391304347827, 0.5335365853658537, 0.5747282608695652, 0.600609756097561, 0.34646739130434784, 0.600609756097561, 0.4565217391304348, 0.5945121951219512, 0.5665760869565217, 0.5579268292682927, 0.10190217391304347, 0.5762195121951219, 0.09782608695652173, 0.5426829268292683, 0.11005434782608697, 0.5884146341463414, 0.11005434782608697]
    skeleton = np.array(data[5:])
    return skeleton

def joint_joint_distance(j1, j2):
    x0,y0,z0 = j1[0],j1[1],j1[2] 
    x1,y1,z1 = j2[0],j2[1],j2[2] 
    height = math.sqrt((x0-x1)**2 + (y0-y1)**2 + (z0-z1)**2)
    return height


def get_a_normalized_standing_skeleton():
    x = get_an_example_of_standing_skeleton()

    NECK = 1
    L_THIGH = 8
    R_THIGH = 11

    # Remove offset by setting neck as origin                        #MODIFIED
    x0, y0, z0 = get_joint(x, NECK)
    x[::3] -= x0
    x[1::3] -= y0
    x[2::3] -= z0


    # Scale the skeleton by taking neck-thigh distance as height
    x0, y0, z0 = get_joint(x, NECK)                                       #MODIFIED
    j2 = (x0, y0, z0)
    x11, y11, z11 = get_joint(x, L_THIGH)
    x12, y12, z12 = get_joint(x, R_THIGH)
    x1 = (x11 + x12) / 2
    y1 = (y11 + y12) / 2
    z1 = (z11 + z12) / 2
    j1 = (x1, y1, z1)
    d1 = joint_joint_distance(j1, j2)
    # height = abs(y0 - d1)
    x /= d1
    return x


def draw_skeleton_joints(skeleton):                          #TODO Da vedere se togliere o meno 
    x = skeleton[::2]
    y = skeleton[1::2]
    plt.plot(-x, -y, "r*")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    skeleton = get_a_normalized_standing_skeleton()
    draw_skeleton_joints(skeleton)
