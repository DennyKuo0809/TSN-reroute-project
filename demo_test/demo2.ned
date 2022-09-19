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


network demo2
{
    @display("bgb=1821.1549,1020.52997");
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=100,100");
        }
        forwardtable: MacForwardingTable {
            @display("p=123.0675,825.1575");
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
        forward0: StandardHost {
            @display("p=457.9725,415.60498");
        }
        forward1: StandardHost {
            @display("p=821.1225,655.6875");
        }
        forward2: StandardHost {
            @display("p=821.1225,225.95999");
        }
        forward3: StandardHost {
            @display("p=1156.0275,415.60498");
        }
        visualizer: IntegratedCanvasVisualizer {
            @display("p=110.9625,258.24");
        }
    connections:
        host0.ethg++ <--> Eth100M <--> forward0.ethg++;
        host1.ethg++ <--> Eth100M <--> forward1.ethg++;
        host2.ethg++ <--> Eth100M <--> forward2.ethg++;
        host3.ethg++ <--> Eth100M <--> forward3.ethg++;
        forward0.ethg++ <--> Eth100M <--> forward1.ethg++;
        forward0.ethg++ <--> Eth100M <--> forward2.ethg++;
        forward1.ethg++ <--> Eth100M <--> forward3.ethg++;
        forward2.ethg++ <--> Eth100M <--> forward3.ethg++;
}

