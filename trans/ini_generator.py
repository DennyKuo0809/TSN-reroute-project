import enum
import ned_generator
import pickle

header = "[General]\n"
header += "network = TSN_multipath\n"
#############################################################
#   disable automatic MAC forwarding table configuration    #
#############################################################
header += "\n"
header += "# disable automatic MAC forwarding table configuration\n"
header += "*.macForwardingTableConfigurator.typename = \"\"\n"

#################################################
#   enable frame replication and elimination    #
#################################################
header += "\n"
header += "# enable frame replication and elimination\n"
header += "*.*.hasStreamRedundancy = true\"\n"

#########################################
#   enable stream policing in layer 2   #
#########################################
header += "\n"
header += "# enable stream policing in layer 2\n"
header += "*.*.bridging.streamRelay.typename = \"StreamRelayLayer\"\n"
header += "*.*.bridging.streamCoder.typename = \"StreamCoderLayer\"\n"

#####################################################
#   enable automatic stream redundancy configurator #
#####################################################
header += "\n"
header += "# enable automatic stream redundancy configurator\n"
header += "*.streamRedundancyConfigurator.typename = \"StreamRedundancyConfigurator\"\n"

#################
#   visualizer  #
#################
header += "\n"
header += "# visualizer\n"
header += "*.visualizer.streamRedundancyConfigurationVisualizer.displayTrees = true\n"
header += "*.visualizer.streamRedundancyConfigurationVisualizer.lineColor = \"black\"\n"

#####################################
#   bitrate  of network interface   #
#####################################
header += "\n"
header += "*.*.eth[*].bitrate = 10Mbps\n"

class Route():
    def __init__(self, T):
        self.topology = T
        self.app = [[] for _ in range(T.host_num)]
        self.port = [1000 for _ in range(T.host_num)]
        self.type1_route = []
        self.type2_route = []

    def parseStream(self):
        for id, (src, dst, util) in enumerate(self.topology.type1):
            new_src_app = {"role": "send", 
                            "destport": self.port[dst],
                            "dst": self.topology.hosts[dst].name,
                            "util": util,
                            "type": int(1),
                            "flow-id" : int(id)}
            new_dst_app = {"role": "recv", 
                            "localport": self.port[dst]}
            self.port[dst] += 1
            self.app[src].append(new_src_app)
            self.app[dst].append(new_dst_app)
        for id, (src, dst, util, _) in enumerate(self.topology.type2):
            new_src_app = {"role": "send", 
                            "destport": self.port[dst],
                            "dst": self.topology.hosts[dst].name,
                            "util": util,
                            "type": int(2),
                            "flow-id" : int(id)}
            new_dst_app = {"role": "recv", 
                            "localport": self.port[dst]}
            self.port[dst] += 1
            self.app[src].append(new_src_app)
            self.app[dst].append(new_dst_app)
    def parseRouting(self, Type1File, Type2File):
        with open(Type1File, "rb") as f:
            self.type1_route = pickle.load(f)
        
        type2_cycle = []
        with open(Type2File, "rb") as f:
            type2_cycle = pickle.load(f)
        
        for (src, dst, _, _) in self.topology.type2:
            ls = [i for i, n in enumerate(type2_cycle) if n == src]
            ld = [i for i, n in enumerate(type2_cycle) if n == dst]
            
            min_dis = self.topology.host_num * 2
            s_idx = -1
            d_idx = -1
            for i in ld:
                for j in ls:
                    if j < i:
                        if i - j < min_dis:
                            min_dis = i - j
                            s_idx = j
                            d_idx = i
            self.type2_route.append(type2_cycle[s_idx:d_idx+1])

        return 
    def genINI(self):
        #############
        #   Header  #
        #############
        print(header, end="")

        #####################################
        #   Source App  & Destination App   #
        #####################################
        print("# apps", end="")
        for i in range(self.topology.host_num):
            name = self.topology.hosts[i].name
            num = len(self.app[i])
            print(f"\n*.{name}.numApps = {num}\n", end="")

            for j, app in enumerate(self.app[i]):
                buf = "\n"
                if app['role'] == "send":
                    if app['type'] == 1:
                        buf += f"*.{name}.app[{j}].typename = \"UdpSourceApp\"\n"
                        buf += f"*.{name}.app[{j}].io.destAddress = \"{app['dst']}\"\n"
                        buf += f"*.{name}.app[{j}].source.packetNameFormat = \"%M-%m-%c\"\n"
                        buf += f"*.{name}.app[{j}].source.displayStringTextFormat = \"sent %p pk (%l)\"\n"
                        buf += f"*.{name}.app[{j}].source.packetLength = {int(1000*app['util'])}B\n"
                        buf += f"*.{name}.app[{j}].source.productionInterval = 100us\n"
                        buf += f"*.{name}.app[{j}].display-name = \"type{app['type']}_{app['flow-id']}\"\n"
                        buf += f"*.{name}.app[{j}].io.destPort = {app['destport']}\n"
                    elif app['type'] == 2:
                        buf += f"*.{name}.app[{j}].typename = \"UdpBasicApp\"\n"
                        buf += f"*.{name}.app[{j}].destAddresses = \"{app['dst']}\"\n"
                        buf += f"*.{name}.app[{j}].source.packetNameFormat = \"%M-%m-%c\"\n"
                        buf += f"*.{name}.app[{j}].source.displayStringTextFormat = \"sent %p pk (%l)\"\n"
                        buf += f"*.{name}.app[{j}].messageLength = {int(1000*app['util'])}B\n"
                        buf += f"*.{name}.app[{j}].sendInterval = 100us\n"
                        buf += f"*.{name}.app[{j}].startTime = 1ms\n"
                        buf += f"*.{name}.app[{j}].display-name = \"type{app['type']}_{app['flow-id']}\"\n"
                        buf += f"*.{name}.app[{j}].destPort = {app['destport']}\n"
                else:
                    buf += f"*.{name}.app[{j}].typename = \"UdpSinkApp\"\n"
                    buf += f"*.{name}.app[{j}].io.localPort = {app['localport']}\n"
                print(buf, end="")

        #####################
        #   Routing Path    #
        #####################

        print("\n# seamless stream redundancy configuration")
        print("*.streamRedundancyConfigurator.configuration = [\n", end="")
        for i, p in enumerate(self.type1_route):
            buf = "{"
            buf += f"name: \"S1-{i}\", packetFilter: \"*-type1_{i}-*\", source: \"{self.topology.hosts[p[0]].name}\", destination: \"{self.topology.hosts[p[-1]].name}\","
            buf += f"trees: [[[{self.topology.hosts[p[0]].name}"
            for j in p[1:-1]:
                buf += f", \"{self.topology.hosts[j].switch_name}\""
            buf += f", \"{self.topology.hosts[p[-1]].name}\"]]]"
            buf += "},"
            print(buf)
        for i, p in enumerate(self.type2_route):
            buf = "{"
            buf += f"name: \"S2-{i}\", packetFilter: \"*-type2_{i}-*\", source: \"{self.topology.hosts[p[0]].name}\", destination: \"{self.topology.hosts[p[-1]].name}\","
            buf += f"trees: [[[{self.topology.hosts[p[0]].name}"
            for j in p[1:-1]:
                buf += f", \"{self.topology.hosts[j].switch_name}\""
            buf += f", \"{self.topology.hosts[p[-1]].name}\"]]]"
            buf += "},"
            print(buf)
        print("]\n")


        '''
        *.streamRedundancyConfigurator.configuration = [{name: "S1", packetFilter: "*-app1-*", source: "source", destination: "destination",
                                                 trees: [[["source", "s1", "s2a", "s3a", "destination"]]]},
	    {name: "S2", packetFilter: "*-app0-*", source: "source", destination: "destination",
                                                 trees: [[["source", "s1", "s2b", "s3b", "destination"]]]}]
        '''

if __name__ == "__main__":
    T = ned_generator.Topology()
    T.fromFie("5.in")
    R = Route(T)
    R.parseRouting("Type1-route.pickle", "Type2-route.pickle")
    # print(f"type1 routing : \n{R.type1_route}\ntype2 routing: \n{R.type2_route}")
    R.parseStream()
    R.genINI()