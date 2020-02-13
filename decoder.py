import pathlib
import csv
import numpy
import pandas

class S1TDecoder:
    def __init__(self, path:pathlib.Path):
        self.name = path.name
        with open(path) as fp:
            self.__array = list(csv.reader(fp, delimiter="\t"))
            self.__array = pandas.DataFrame(self.__array)
        # self.__header = self.__array[0:10]
        self.__wave_data = self.__array.iloc[10:]
        self.__wave_data.columns = self.__array.iloc[8]
        self.__wave_data = self.__wave_data.set_index('Number')

    def y(self):
        return numpy.array(self.__wave_data["Load"], dtype=float)

    def x(self):
        x = numpy.array(self.__wave_data["Position"], dtype=float)
        return numpy.arange(x.min(), x.max(), (x.max()-x.min())/len(x))

    def positions(self):
        return self.x()

    def loads(self):
        return self.y()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    folder = r"C:\Users\J100047187\Pictures\HKMC\Fretwork tensile"
    folder = pathlib.Path(folder)
    folders = list(folder.glob("*.S1T"))
    data = S1TDecoder(folders[0])
    
    plt.plot(data.x(), data.y())
    plt.grid()
    plt.show()
    
