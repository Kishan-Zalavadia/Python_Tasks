# convert the array to dictonary and then print that
def arr_to_dict(arr):
    dict = {}
    for index,val in enumerate(arr):
        dict[index] = val
    print(dict)

# another way to do this
def arr_to_dict2(arr): 
    print({index:val for index,val in enumerate(arr)})