"""
HDF5 files tools for HDF5 Manipulator
"""

import h5py


def load(filename):

    """Load hdf5 file to data dictionary and return it.

    Keyword arguments:
    filename -- the full path to hdf5 file
    """

    f = h5py.File(filename, 'r')

    data = {}
    attrs = {}

    for key in f:
        data[key] = f[key][...]
        
    for key in f.attrs:
        attrs[key] = f.attrs[key]


    f.close()

    return data, attrs


def save(filename, data, attrs):

    """Create hdf5 file with given data.

    Keyword arguments:
    filename -- the full path to hdf5 file
    data -- dictionary with data
    """

    f = h5py.File(filename, 'w')

    for key in data:
        f.create_dataset(key, data[key].shape, dtype=data[key].dtype,
                         compression='gzip')[...] = data[key]
    
    for key in attrs:
        f.attrs[key] = attrs[key]
    
    f.close()


def save_subset(filename, data, begin, end):

    """Create hdf5 file with subset [begin, end) of given data.

    Keyword arguments:
    filename -- the full path to hdf5 file
    data -- dictionary with data
    begin -- start saving from index=i
    end -- finish savin at index=end
    """

    subset = {}

    for key in data:
        subset[key] = data[key][begin:end]

    save(filename, subset)


def save_subset_big(filename, data, begin, end):

    """Create hdf5 file with subset [begin, end) of given data.

    Keyword arguments:
    filename -- the full path to hdf5 file
    data -- input file
    begin -- start saving from index=i
    end -- finish savin at index=end
    """

    o = h5py.File(filename, 'w')

    for key in data:
        shape = list(data[key].shape)
        shape[0] = end - begin
        o.create_dataset(key, shape, dtype=data[key].dtype,
                         compression='gzip')[...] = data[key][begin:end]

    o.close()
