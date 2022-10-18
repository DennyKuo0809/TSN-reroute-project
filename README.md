### Usage

#### Step 1: import cycle detection project 
```sh=
$ git clone https://github.com/Ching-Chu-Lin/cycle.git
```

#### Step 2: generate routing result
```sh=
# Type1 route
$python3.9 cycles/main.py {input_file} {method}

# Type2 route
$ python3.9 cycles/johnson_modify.py {input file} {constant}
```

#### Step 3: generate ned & ini file
```sh=
$ python3.9 src/ini_generator.py > {path to output.ini}
$ python3.9 src/ned_generator.py > {path to output.ned}
```

#### Step 4: run simulation (in command line)
```sh=
$ cd {omnetpp directory} ; . setenv
$ cd {inet directory} ; . setenv

$ cd {directory with ini & ned}
$ inet {path to ini} -u Cmdenv
```

#### Step 5: export the result files to csv foramt
```sh=
$ opp_scavetool x {-f filter} -F CSV-R -o {path to output.csv}
```

#### Step 6: analysis the result
### Still in progress
- keep in mind
  - maybe : $ python3.9 {analysis.py} {path to csv} 
  - TSN_multipath.destination.app[0].sink
  - meanBitLifeTimePerPacket:histogram
  - https://inet.omnetpp.org/docs/showcases/measurement/endtoenddelay/doc/index.html
