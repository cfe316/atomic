# Compile and link tstxxdata_15 FORTRAN
#
f77 -o test.out test.for \
xxdata_15.for \
xxrptn.for \
xxmkrp.for \
i4unit.for \
i4fctn.for \
r8fctn.for \
xxhkey.for \
xxword.for \
xxcase.for \
i4eiz0.for \
xfelem.for \
xxslen.for 

# Run the program
#
./test.out




