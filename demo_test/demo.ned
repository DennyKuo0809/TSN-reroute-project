//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package inet.tutorials.configurator.demo_test;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.ethernet.Eth100M;
import inet.node.ethernet.Eth10M;
import inet.node.ethernet.EthernetSwitch;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;
import inet.linklayer.ethernet.common.MacForwardingTable;
import inet.linklayer.configurator.MacForwardingTableConfigurator;


network demo
{
    @display("bgb=1704.7875,936.12");
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=100,100");
        }
        macTableConfigurator: MacForwardingTableConfigurator{
            @display("p=100,100");
        }
        host0: StandardHost {
            @display("p=268.32748,417.6225");
        }
        host1: StandardHost {
            @display("p=821.1225,825.1575");
        }
        host2: StandardHost {
            @display("p=821.1225,68.595");
        }
        host3: StandardHost {
            @display("p=1357.7775,417.6225");
        }
        switch0: EthernetSwitch {
            @display("p=457.9725,415.60498");
        }
        switch1: EthernetSwitch {
            @display("p=821.1225,655.6875");
        }
        switch2: EthernetSwitch {
            @display("p=821.1225,225.95999");
        }
        switch3: EthernetSwitch {
            @display("p=1156.0275,415.60498");
        }
        visualizer: IntegratedCanvasVisualizer {
            @display("p=110.9625,258.24");
        }
    connections:
        host0.ethg++ <--> Eth100M <--> switch0.ethg++;
        host1.ethg++ <--> Eth100M <--> switch1.ethg++;
        host2.ethg++ <--> Eth100M <--> switch2.ethg++;
        host3.ethg++ <--> Eth100M <--> switch3.ethg++;
        switch0.ethg++ <--> Eth100M <--> switch1.ethg++;
        switch0.ethg++ <--> Eth100M <--> switch2.ethg++;
        switch1.ethg++ <--> Eth100M <--> switch3.ethg++;
        switch2.ethg++ <--> Eth100M <--> switch3.ethg++;
}

