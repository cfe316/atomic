import os
import _xxdata_11

parameters = {
    'isdimd' : 200,
    'iddimd' : 40,
    'itdimd' : 50,
    'ndptnl' : 4,
    'ndptn' : 128,
    'ndptnc' : 256,
    'ndcnct' : 100
}

def read_scd(filename):
    fd = open(filename, 'r')

    fortran_filename = 'fort.%d' % fd.fileno()
    os.symlink(filename, fortran_filename)

    iclass = 2 # class number for scd files
    ret =  _xxdata_11.xxdata_11(fd.fileno(), iclass, **parameters)
    os.unlink(fortran_filename)
    return ret

if __name__ == '__main__':
    out = read_scd('scd96_c.dat')
    print out[0]
