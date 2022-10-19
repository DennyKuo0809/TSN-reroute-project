from johnson import simple_cycles
from collections import defaultdict

def parseGraph(inputFile, reduceConst):
    g = defaultdict(list)
    with open(inputFile, "r") as input_file:
        num_vertex = int(input_file.readline().strip())

        for i in range(num_vertex):
            start_vertex, neighbor_util = input_file.readline().strip().split(",")
            neighbor_util = neighbor_util.split(" ")
            j = 0
            for end_vertex, util in zip(neighbor_util[0::2], neighbor_util[1::2]):
                g[start_vertex].append(end_vertex)
    return g

def main():
	g = parseGraph('../trans/5.in', 0)
	print(g)
	print(tuple(simple_cycles(g)))

if __name__ == "__main__":
	main()
