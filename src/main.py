import sys 
import json 

def main(): 
    # Check number of given arguments (should be one JSON file) 
    if len(sys.argv) < 2:
        print("Incorrect number of arguments.")
        sys.exit(1)

    # Read contents of input JSON file with all the paths 
    with open(sys.argv[1], 'r') as file:
        json_data = json.load(file)

    
    return 0

if __name__ == "__main__": 
    main()