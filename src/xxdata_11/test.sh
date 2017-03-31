# Compile and link test Fortran program
#
gfortran -o test.out test.for \
xxdata_11.for \
xxrptn.for \
i4unit.for \
i4fctn.for \
xxword.for \
xxcase.for \
xfelem.for \
xxslen.for 

# Run the program
#
./test.out
