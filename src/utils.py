

def manhat(a,b):
    # Return manhattan distance between two coordinates
    ax, ay = a
    bx, by = b
    if ax > bx:
        diffx = ax - bx
    else:
        diffx = bx - ax
    if ay > by:
        diffy = ay - by
    else:
        diffy = by - ay
    return diffx + diffy