# split-json.py 

import json
import argparse


def filterData (entry, Month, Year, Interface):
    # Filter the data based on the Month, Year, and Interface
    if entry['interface'] != Interface:
        return False

    if entry['direction'] != 'downlink':
        return False

    if entry['type'] != 'iperf':
        return False

#    print('Checking the timestamp')
#    print('  Entry: ', entry['timestamp'])
#    print('  Month: ', Month, ' vs. ', entry['timestamp'].split('-')[1])

    if int(entry['timestamp'].split('-')[1]) != Month:
#        print('Filtering on month')
        return False

    if entry['timestamp'].split('-')[0] != str(Year):
        return False

#    print('Do not filter')
    return True



# Are we being executed directly?
if __name__ == "__main__":
    # Define the various arguments via argparse
    parser = argparse.ArgumentParser(description='Split up the JSON')
    parser.add_argument('InputJSON', type=str, help='Filename as an input')
    parser.add_argument('Month', type=int, help='Month to include')
    parser.add_argument('Year', type=int, help='Year to include')
    parser.add_argument('Interface', type=str, help='Interface to include')
    parser.add_argument('OutputFile', type=str, help='Filename as an output')    

    args = parser.parse_args()

    theData = json.loads(open(args.InputJSON).read())
    print('Detected ', len(theData), ' entries in the JSON file')

    NumEntries = len(theData)

    filteredData = list(filter(lambda entry: filterData(entry, args.Month, args.Year, args.Interface), theData))

    filteredData.sort(key=lambda entry: entry['timestamp'])

    print('Post Filtering: ', len(filteredData), ' entries in the JSON file')

    with open(args.OutputFile, 'w') as f:
        # Write the JSON to the file
        f.write(json.dumps(filteredData, indent=4))
        # Is this really needed?
        f.close()
