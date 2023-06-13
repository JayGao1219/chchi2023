import matplotlib.pyplot as plt

def write_data(filename):
    # 绘制 test.txt 中的数据
    with open(filename+".txt","r") as f:
        data = f.read()
        data = eval(data)
        plt.plot(data)
        plt.savefig(filename+".png")

write_data("df")