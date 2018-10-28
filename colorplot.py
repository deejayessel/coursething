import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def plot(filename):
    with open(filename,'r') as f:
        lines = f.readlines()

    def clean(s):
        return s.replace("'",'').replace('[','').replace(']','').replace('\n','')

    m = []
    for line in lines[1:-1]:
        m.append([float(clean(w)) for w in line.split(', ')])

    # transpose of m
    mt = [[ m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
        
    # make img
    cmap = mpl.colors.Colormap('Greys')
    norm = mpl.colors.Normalize()
    img = plt.imshow(mt, aspect='auto', cmap="cividis")

    # make color bar
    plt.colorbar(img, cmap=cmap, norm=norm)

    plt.title('Class distribution across hours of the week')
    plt.ylabel('Time of day')
    plt.xlabel('Day of the week')
    plt.savefig('o.png')

if __name__ == '__main__':
    plot('dumbass')

