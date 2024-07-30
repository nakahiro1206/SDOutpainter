import numpy as np
import matplotlib.pyplot as plt
import warnings
# warnings.simplefilter('error', category=RuntimeWarning)
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

H = 512
W = 512
def filter(x, y):
    alpha = 10 # slope
    # return np.where(
    #     x+y>H, 
    #     1/2 - 1/np.pi * np.arctan(alpha*(x-y)/(H+W-x-y)) * (1-((x+y-H)/H)**4), 
    #     1/2 - 1/np.pi * np.arctan(alpha*(x-y)/(x+y)) * (1-((x+y-H)/H)**4)
    # )
    return 1/2 - 1/np.pi * np.arctan(alpha*(x-y)/(x+y)) * (1-((x+y-H)/H)**8)

def f2(x, y):
    # return (1/x)/((1/x))
    return (1/x)/((1/x) + (1/y))
    # return (1/x)/((1/x) + (1/(W-x)))
    # return (1/x)/((1/x) + (1/y) + (1/(H-y)))
    return (1/x)/((1/x) + (1/y) + (1/(W-x)))
    return (1/x)/((1/x) + (1/y) + (1/(H-y)) + (1/(W-x)))

step = 50
x = np.linspace(0, H, step+2)[1:-1]
y = np.linspace(0, W, step+2)[1:-1]

X, Y = np.meshgrid(x, y)
# Z = filter(X, Y)
Z = f2(X, Y)

# print(Z)
# i = 0
# for y in Z:
#     for x in y:
#         if np.isnan(x):
#             print(i//H, i%H)
#         i+=1

fig = plt.figure()
ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# ax.view_init(60, 35)
plt.show()
plt.savefig("../../assets/3d_plot.png")