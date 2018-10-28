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
    fig = plt.figure(figsize=(5.0,8.0))
    img = plt.imshow(mt, aspect='auto', cmap="cividis")

    # make color bar
    plt.colorbar(img, cmap=cmap, norm=norm)

    plt.title('Class distribution across hours of the week', pad=20, loc='center')
    plt.ylabel('Time of day', labelpad=15)
    plt.xlabel('Day of the week', labelpad=15)
    plt.xticks(list(range(5)), 'MTWRF')
    plt.savefig('o.png',
                orientation='portrait',
                quality=90,
                bbox_inches='tight',
                pad_inches=0.5)

if __name__ == '__main__':
    plot('dumbass')

