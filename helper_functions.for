C Helper function to open a file pointer
      subroutine helper_open_file(iunit, filename)

      character filename*120
      integer iunit

      iunit = 10
      open(unit=iunit, file=filename, status='old')

      end


      subroutine helper_close_file(iunit)

      close(iunit)

      end
