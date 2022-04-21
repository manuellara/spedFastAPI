from csv_diff import load_csv, compare
import json

# compares Aeries snapshot to Aeries snapshot + updated values
def compareCSV(csv1, csv2, key1, key2):

    diff = compare(
        load_csv(open(csv1), key=key1),
        load_csv(open(csv2), key=key2)
    )

    try:
        with open('compare_data.json', 'w') as outfile:
            json.dump(diff, outfile, indent=4)
    except Exception as e:
        print(e)

    # print(diff)




# compares SEIS snapshot to SEIS snapshot after invalid District IDs were filtered out
def compareSEIS(csv1, csv2, key1, key2):
    diff = compare(
        load_csv(open(csv1), key=key1),
        load_csv(open(csv2), key=key2)
    )

    try:
        with open('compare_SEIS.json', 'w') as outfile:
            json.dump(diff, outfile, indent=4)
    except Exception as e:
        print(e)

    # print(diff)