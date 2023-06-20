import math

radius = 160

# Convert degrees to radians
def toRadian(theta):
    return theta * math.pi / 180

# Convert radians to degrees
def toDegrees(theta):
    return theta * 180 / math.pi

# Calculate the gradient (slope) between two points
def getGradient(p1, p2):
    if p1[0] == p2[0]:
        # Vertical line, set gradient to 90 degrees in radians
        m = toRadian(90)
    else:
        # Calculate the slope of the line
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return m

# Calculate the angle from the gradient
def getAngleFromGradient(gradient):
    return math.atan(gradient)

# Calculate the angle between two points and the origin
def getAngle(pos, origin):
    m = getGradient(pos, origin)
    thetaRad = getAngleFromGradient(m)
    theta = round(toDegrees(thetaRad), 2)
    return theta

# Calculate the position on the circumference of a circle
def getPosOnCircumeference(theta, origin):
    theta = toRadian(theta)
    x = origin[0] + radius * math.cos(theta)
    y = origin[1] + radius * math.sin(theta)
    return (x, y)


