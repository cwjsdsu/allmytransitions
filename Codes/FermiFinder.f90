!
! code FermiFinder
!
! searches a .str file for Fermi transitions
! which is easy: same J, T, energy
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
integer       :: nFermi


unitin  = 3
unitout = 4

print*,' Welcome to FERMI FINDER! '

!........... OPEN INPUT FILE.................

success = .false.

do while(.not.success)
	print*,' Enter name of INPUT .str file '
	read(5,'(a)')filein
	ilastin = index(filein,' ')-1
	inquire(file=filein(1:ilastin)//".str",exist=filelives)
	if(.not.filelives)then
		print*,' file ',filein(1:ilastin)//".str",' does not exist '
		cycle
	end if
	open(unit=unitin,file=filein(1:ilastin)//".str",status='old')
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
nfermi = 0
do iparent = 1,nparent
	read(unitin,*)i,eparent,xJp,xTp
100 format(i5,f10.3,f5.1,f5.1,'    ! parent  Energy  J     T')
	
	read(unitin,*)nd      ! # of daughters here
	
	do id = 1,nd
		read(unitin,*)i,edaughter,xJd,xTd,bgt
		ndaughter = max(i,ndaughter)       ! find maximal daughter label
101 format(i5,f10.3,f5.1,f5.1,f10.4, '    ! daughter  Energy  J     T   strength ')

!................ IDENTIFY TRANSITIONS ...........
if( xJp == xJd .and. xTP == xTd .and. abs(edaughter-eparent)< .001)then
	write(6,'("Found a Fermi!  Parent state = ",i5,", daughter state = ",i5, & 
	  ", Energy = ",f10.5,"; J, T = ",2f4.1 )'  )iparent,i,eparent,xJp,xTp
	  nfermi = nfermi + 1
  end if
		
	end do

	read(unitin,'(a60)')dummyline   ! summed strength
	
end do


print*,' There are a maximum of ',ndaughter,' daughter states '
!...............GET ENERGY SHIFTS...............

print*,' There are total of ',nfermi,' Fermi transitions in this file '

end
