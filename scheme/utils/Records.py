def convertTupleToString(val):
    result = '--'.join([str(i).replace("-", "-0") for i in val])
    return result

def convertStringToTuple(val):
    result = tuple([str(i).replace("-0", "-") for i in val.split("--")])
    return result