import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def plot(filename, cmap):
    with open(filename,'r') as f:
        lines = f.readlines()

    def clean(s):
        return s.replace("'",'').replace('[','').replace(']','').replace('\n','')

    m = []
    for line in lines:
        m.append([float(clean(w)) for w in line.split(', ')])

    # transpose of m
    mt = [[ m[j][i] for j in range(len(m))] for i in range(len(m[0]))]
        
    # make img
    #cmap = mpl.colors.Colormap('Greys')
    norm = mpl.colors.Normalize()
    fig = plt.figure(figsize=(5.0,8.0))
    img = plt.imshow(mt, aspect='auto', cmap=cmap)

    # make color bar
    plt.colorbar(img, cmap=cmap, norm=norm)

    plt.title('Class distribution across hours of the week', pad=20, loc='center')
    plt.ylabel('Time of day', labelpad=15)

    def hourlist():
        l = []
        for i in range(8*60, 1300, 60): #8:00 am to 9:40 pm
            hour = i//60
            min = i % 60
            l.append(f"{hour}:{min}0")
        return l

    ticks = hourlist()
    plt.yticks(range(-1,(1300-8*60)//5,12), ticks)

    plt.xlabel('Day of the week', labelpad=15)
    plt.xticks(list(range(5)), 'MTWRF')

    plt.savefig(f'{filename}.png',
                orientation='portrait',
                quality=90,
                bbox_inches='tight',
                pad_inches=0.5)

if __name__ == '__main__':
    plot('csci','Greys')
    plot('div1',"Reds")
    plot('div2',"Greens")
    plot('div3',"Blues")
    plot('all',"Purples")
