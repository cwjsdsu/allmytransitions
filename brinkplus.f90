!
! code BRINKSMANSHIP
!
! applies the brink hypothesis to B(GT) calculations
!
! namely, reads in a file of (same parity) B(GT)
! user gives it energies of first odd parity state
! and it creates additional data from the first, but shifted up in energy
!
! by CWJ @ SDSU March 2016
!


implicit none

character(60) :: filein,fileout,dummyline
integer       :: ilastin,ilastout
integer       :: unitin,unitout
character     :: ychar
logical       :: success,filelives

real          :: eshiftparent,eshiftdaughter
integer       :: nparent,ndaughter
integer       :: iparent,nd,id
real          :: eparent, edaughter
real          :: xJp,xTp,xJd,xTd
integer       :: i
real          :: bgt


unitin  = 3
unitout = 4

print*,' Welcome to BRINKSMANSHIP! '
print*,' Beta PLUS only! '

!........... OPEN INPUT FILE.................

success = .false.

do while(.not.success)
	print*,' Enter name of INPUT isotope file '
	read(5,'(a)')filein
	ilastin = index(filein,' ')-1
	inquire(file=filein(1:ilastin)//"usdbBplus.str",exist=filelives)
	if(.not.filelives)then
		print*,' file ',filein(1:ilastin)//"usdbBplus.str",' does not exist '
		cycle
	end if
	open(unit=unitin,file=filein(1:ilastin)//"usdbBplus.str",status='old')
	success = .true.
end do ! while not success

!........... OPEN OUTPUT FILE.................

success = .false.

do while(.not.success)
!	print*,' Enter name of OUTPUT .str file '
!	read(5,'(a)')fileout
!	ilastout = index(fileout,' ')-1
!	if(fileout(1:ilastout)==filein(1:ilastin))then
!		print*,' The two files cannot be the same '
!		cycle
!	end if
	
	inquire(file=filein(1:ilastin)//"usdbBplusBrink.str",exist=filelives)
	if(filelives)then
		print*,' file ',filein(1:ilastin)//"usdbBplusBrink.str",' alreadys exists; overwrite(y/n)? '
		read(5,'(a)')ychar
		if(ychar=='n' .or. ychar=='N')cycle
		open(unit=unitout,file=filein(1:ilastin)//"usdbBplusBrink.str",status='old')
	else
			open(unit=unitout,file=filein(1:ilastin)//"usdbBplusBrink.str",status='new')
	end if
		
	success = .true.
end do ! while not success

!.............. READ IN PRELIMINARY DATA..............

read(unitin,'(a60)')dummyline
write(unitout,'(a60)')dummyline
read(unitin,'(a60)')dummyline
write(unitout,'(a60)')dummyline

read(unitin,*)nparent
print*,' There are ',nparent,' parent states '
99 format(i4,'     ! # parents ')
write(unitout,99)nparent*2
ndaughter = 0

do iparent = 1,nparent
	read(unitin,*)i,eparent,xJp,xTp
100 format(i5,f10.3,f5.1,f5.1,'    ! parent  Energy  J     T')
    write(unitout,100)i,eparent,xJp,xTP
	
	read(unitin,*)nd      ! # of daughters here
       write(unitout,102)nd
102 format(i4,'     ! # daughters ')	
	do id = 1,nd
		read(unitin,*)i,edaughter,xJd,xTd,bgt
		write(unitout,101)i,edaughter,xJd,xTd,bgt
		ndaughter = max(i,ndaughter)       ! find maximal daughter label
101 format(i5,f10.3,f5.1,f5.1,f10.4, '    ! daughter  Energy  J     T   strength ')
		
	end do

	read(unitin,'(a60)')dummyline   ! summed strength
	write(unitout,'(a60)')dummyline	
	
end do


print*,' There are a maximum of ',ndaughter,' daughter states '
!...............GET ENERGY SHIFTS...............

print*,' Enter excitation of first opposite parity state in PARENT '
read*,eshiftparent

print*,' Enter excitation of first opposite parity state in DAUGHTER '
read*,eshiftdaughter


rewind(unitin)
read(unitin,'(a60)')dummyline
read(unitin,'(a60)')dummyline
read(unitin,'(a60)')dummyline

do iparent = 1,nparent
	read(unitin,*)i,eparent,xJp,xTp
200 format(i5,f10.3,f5.1,f5.1,'    ! parent  OPPOSITE PARITY ')
    write(unitout,200)i+nparent,eparent+eshiftparent,xJp,xTP
	
	read(unitin,*)nd      ! # of daughters here
    write(unitout,102)nd
	
	do id = 1,nd
		read(unitin,*)i,edaughter,xJd,xTd,bgt
		write(unitout,201)i+ndaughter,edaughter+eshiftdaughter,xJd,xTd,bgt
		ndaughter = max(i,ndaughter)       ! find maximal daughter label
201 format(i5,f10.3,f5.1,f5.1,f10.4, '    ! daughter  OPPOSITE PARITY ')
		
	end do
	

	read(unitin,'(a60)')dummyline  ! summed strength
	write(unitout,'(a60)')dummyline	
end do


end
