import ini_generator
import ned_generator




def main():
    T = ned_generator.Topology()
    T.fromFie("5.in")
    R = ini_generator.Route(T)
    R.parseRouting("Type1-route.pickle", "Type2-route.pickle")
    #print(f"type1 routing : \n{R.type1_route}\ntype2 routing: \n{R.type2_route}")
    R.parseStream()
    R.genINI()

if __name__ == "__main__":
    main()
