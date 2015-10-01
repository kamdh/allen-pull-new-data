import numpy as np

def extract_volume(load_dir, file_name_prefix, dtype):
    f = open(os.path.join(load_dir, file_name_prefix) + '.mhd', 'r')
    header = f.read()
    f.close()
    f = open(os.path.join(load_dir, file_name_prefix) + '.raw', 'r')
    raw = f.read()
    f.close()
    arr = np.frombuffer(raw, dtype=dtype)
    # parse the meta image header.  each line should be a 'key = value' pair.
    metaLines = header.split('\n')
    metaInfo = dict(line.split(' = ') for line in metaLines if line)
    # convert values to numeric types as appropriate
    for k,v in metaInfo.iteritems():
        if re.match("^[\d\s]+$",v):
            nums = v.split(' ')
            if len(nums) > 1:
                metaInfo[k] = map(float, v.split(' '))
            else:
                metaInfo[k] = int(nums[0])
    # reshape the array to the appropriate dimensions.  Note the use of the fortran column ordering.
    arr = arr.reshape(metaInfo['DimSize'], order='F')
    return (header,arr,metaInfo)
