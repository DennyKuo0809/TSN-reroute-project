
ned_header = "package inet.tutorials.configurator.demo_test;\n"
ned_header += "import inet.networks.base.TsnNetworkBase;\n"
ned_header += "import inet.node.ethernet.EthernetLink;\n"
ned_header += "import inet.node.tsn.TsnDevice;\n"
ned_header += "import inet.node.tsn.TsnSwitch;\n"
ned_header += "\n"
ned_header += "module LocalTsnSwitch extends TsnSwitch\n"
ned_header += "{\n"
ned_header += "\t@defaultStatistic(\"gateStateChanged:vector\"; module=\"eth[0].macLayer.queue.gate[0]\");\n"
ned_header += "}\n"
ned_header += "network TSN_multipath extends TsnNetworkBase\n"
ned_header += "{\n"


class Tsn_Device():
    def __init__(self, name="", switch_name = ""):
        # There always is a switch for amy device (host)
        self.name = name 
        self.switch_name = switch_name

class Link():
    def __init__(self, src, dst, cap):
        self.src = src
        self.dst = dst
        self.cap = cap

class Type1_Stream():
    def __init__(self, src, dst, util):
        self.src = src
        self.dst = dst
        self.util = util

class Type2_Stream():
    def __init__(self, src, dst, util, num_trans):
        self.src = src
        self.dst = dst
        self.util = util
        self.num_trans = num_trans

class Topology():
    def __init__(self):
        self.input_file = ""
        self.output_file = ""

        self.host_num = 0
        self.edge_num = 0
        self.hosts = []
        self.edges = []

        self.type1_num = 0
        self.type2_num = 0
        self.type1 = []
        self.type2 = []

        self.trans_num = 0
        

    def fromFie(self, file_name):
        self.input_file = file_name
        with open(file_name, "r") as input_file:
            # parse number of vertex
            self.host_num = int(input_file.readline().strip())

            # parse graph
            for i in range(self.host_num):
                self.hosts.append(Tsn_Device("host" + str(i), "switch" + str(i)))

                src, capcity = input_file.readline().strip().split(",")
                capcity = capcity.split(" ")
                for dst, cap in zip(capcity[0::2], capcity[1::2]):
                    self.edges.append(Link(int(src), int(dst), float(cap)))

            # parse input to be routed: type1
            self.type1_num = int(input_file.readline().strip())
            for _ in range(self.type1_num):
                src, dst, util = input_file.readline().strip().split(" ")
                self.type1.append(Type1_Stream(int(src), int(dst), float(util)))

            # parse expected utilizations: type2 (util, edge constraint)
            self.type2_num = int(input_file.readline().strip())
            for _ in range(self.type2_num):
                src, dst, util, edge_constraint = input_file.readline().strip().split(" ")
                self.type2.append(Type2_Stream(int(src), int(dst), float(util), int(edge_constraint)))

            # parse constraint 2: max number of transfer
            self.trans_num = int(input_file.readline().strip())

    def genNed(self, file_name=""):
        # if file_name were not specified, output the result to stdout
        
        # header
        print(ned_header)

        # submodule (host & switch)
        print("\tsubmodules:\n")
        for device in self.hosts:
            submodule = "\t\t{}: TsnDevice {\n".format(device.name)
            submodule += "\t\t\t@display(\"p=300,200\");\n"
            submodule += "\t\t}\n"
            submodule += "\t\t{}: LocalTsnSwitch {\n".format(device.switch_name)
            submodule += "\t\t\t@display(\"p=300,200\");\n" 
            submodule += "\t\t}\n"
            print(submodule)

        # connection (edge)
        print("\tconnections:\n")
        for device in self.hosts:
            print("{}.ethg++ <--> EthernetLink <--> {}.ethg++".format(device.name, device.switch_name))

        for edge in self.edges:
            print("{}.ethg++ --> EthernetLink --> {}.ethg++".format(self.hosts[edge.src].switch_name, self.hosts[edge.dst].switch_name))

        # end
        print("}")