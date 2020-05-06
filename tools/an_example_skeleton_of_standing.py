
import numpy as np
import matplotlib.pyplot as plt
import math

def get_body_height(x):                                                       #MODIFIED
        ''' Compute height of the body, which is defined as:
            the distance between `neck` and `thigh`.
        '''

        NECK = 0
        L_THIGH = 7
        R_THIGH = 10
        NaN = 0
        x0, y0, z0 = get_joint(x, NECK)

        # Get average thigh height
        x11, y11, z11 = get_joint(x, L_THIGH)
        x12, y12, z12 = get_joint(x, R_THIGH)
        if y11 == NaN and y12 == NaN:  # Invalid data
            return 1.0
        if y11 == NaN:
            x1, y1, z1 = x12, y12, z12
        elif y12 == NaN:
            x1, y1, z1 = x11, y11, z11
        else:
            x1, y1, z1 = (x11 + x12) / 2, (y11 + y12) / 2, (z11 + z12) / 2              #MODIFIED

        # Get body height
        height = math.sqrt((x0-x1)**2 + (y0-y1)**2 + (z0-z1)**2)                        #MODIFIED

        return height

def get_joint(x, idx):                                                #MODIFIED
    px = x[3*idx]
    py = x[3*idx+1]
    pz = x[3*idx+2]
    return px, py, pz

 
def set_joint(x, idx, px, py, pz):                                    #MODIFIED
    x[3*idx] = px
    x[3*idx+1] = py
    x[3*idx+2] = pz
    return 

def get_an_example_of_standing_skeleton():  
    data=[]
    h_list = [-40.4564, -163.091, -0.521563, 
    -19.4528, -146.612, 1.46159, 
    -20.2358, -147.348, 19.1843, 
    -13.1145, -120.269, 28.0371, 
    -20.1037, -94.3607, 30.0809, -19.2473, -146.679, -16.1136, -14.7958, -118.804, -20.6738, -22.611, -93.8793, -17.7834, -17.623, -90.4888, 15.0403, -17.3973, -46.9311, 15.9659, -13.1719, -7.60601, 13.4749, -12.3267, -91.5465, -6.55368, -12.6556, -47.0963, -4.83599, -10.8069, -8.31645, -4.20936, -28.7043, -167.333, -7.15903, -38.7164, -166.851, -3.25917, -30.0718, -167.264, 8.18371, -39.0433, -166.677, 2.55916]
    high = get_body_height(h_list)
    rng = range(0, len(h_list))
    for xi in rng:
        data.append(h_list[xi]/high)
    '''
    data = [7, 67, 7041, "stand", "stand_03-08-20-24-55-587/00055.jpg", 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 
    3.65623635e-01, -3.36195466e-01,  4.00768937e-02, 
     4.62836267e-01, -2.21966707e-01, 8.05059761e-01,  
     4.58144372e-01, -8.76318647e-02,  1.45736597e+00, 
     3.77202670e-01,  3.59908874e-01, -2.37323940e-04, 
      2.93909086e-01, 5.33992392e-01,  7.39852635e-01, 
       3.71150909e-01,  5.06039429e-01, 1.39334546e+00, 
        3.25954938e-01,  2.39599876e-01, -3.43692529e-02,
         1.61406859e+00,  1.19848589e-01,  1.12318538e+00, 
          1.30380551e+00, 2.54662827e-01,  2.07461278e+00,  
          1.15117062e+00,  6.24156503e-01, -2.49546122e-02, 
           1.31848874e+00,  3.62452987e-01,  1.03388513e+00,
            1.01018786e+00,  3.35272276e-01,  2.05505800e+00]'''
    skeleton = np.array(data[:])
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
    # draw_skeleton_joints(skeleton)
