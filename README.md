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
$ python3.9 src/main.py > {output.ini}
$ python3.9 src/ned_generator.py > {output.ned}
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
$ opp_scavetool x {-f filter} -F CSV-R -o {output.csv}
```

#### Step 6: analysis the result
### Still in progress
