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

import inet.networks.base.TsnNetworkBase;
import inet.node.ethernet.EthernetLink;
import inet.node.tsn.TsnDevice;
import inet.node.tsn.TsnSwitch;

channel Eth80M extends EthernetLink
{
    datarate = 80Mbps;
}

module LocalTsnSwitch extends TsnSwitch
{
    @defaultStatistic("gateStateChanged:vector"; module="eth[0].macLayer.queue.gate[0]");
}

network TSN_multipath extends TsnNetworkBase
{
    submodules:
        source: TsnDevice {
            @display("p=300,200");
        }
        s1: LocalTsnSwitch {
            @display("p=500,200");
        }
        s2a: LocalTsnSwitch {
            @display("p=700,100");
        }
        s3a: LocalTsnSwitch {
            @display("p=900,100");
        }
        s2b: LocalTsnSwitch {
            @display("p=700,300");
        }
        s3b: LocalTsnSwitch {
            @display("p=900,300");
        }
        destination: TsnDevice {
            @display("p=1100,200");
        }
    connections:
        s3a.ethg++ <--> EthernetLink <--> destination.ethg++;
        s3b.ethg++ <--> EthernetLink <--> destination.ethg++;
        s2a.ethg ++ <--> EthernetLink <--> s2b.ethg ++;
        s2a.ethg++ <--> EthernetLink <--> s3a.ethg++;
        s2b.ethg++ <--> EthernetLink <--> s3b.ethg++;
        s1.ethg++ <--> EthernetLink <--> s2a.ethg++;
        s1.ethg++ <--> EthernetLink <--> s2b.ethg++;
        source.ethg++ <--> EthernetLink <--> s1.ethg++;
}