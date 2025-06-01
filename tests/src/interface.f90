! SPDX-License-Identifier: GPL-2.0+

module face

    use iso_fortran_env, only: output_unit, real128
    
    implicit none
    
    ! Parameters
    integer, parameter :: dp = selected_real_kind(p=15)
    integer, parameter :: qp = selected_real_kind(p=30)
    integer, parameter :: lp = selected_int_kind(16)
    
    
    interface convert
        module procedure convert_int
        module procedure convert_real
        module procedure convert_real_dp
        module procedure convert_str
        module procedure convert_cmplx
    end interface convert
    

    interface operator(+)
        procedure :: my_add, my_add2
    end interface 
    
    
    interface operator(-)
        procedure :: my_sub
    end interface

    interface assignment (=)
        procedure :: my_eq
    end interface 
    
    interface operator(.MYUN.)
        procedure :: my_unnary
    end interface 
    
    
    type my_type
        real :: a,b
    end type my_type
    
    
    contains
    
    
    real function my_add(a,b)
        type(my_type), intent(in) :: a
        integer, intent(in) :: b
        
        my_add = a%a*2 +b*2
    end function my_add
    
    real function my_add2(a,b)
        type(my_type), intent(in) :: a
        real, intent(in) :: b
        
        my_add2 = a%a*2 +b*2
    end function my_add2

    real function my_sub(a,b)
        type(my_type), intent(in) :: a
        integer, intent(in) :: b
        
        my_sub = a%a*2 - b*2
    end function my_sub
    
    subroutine my_eq(a, b)
        type(my_type), intent(inout)  :: a
        integer,intent(in) :: b
        
        a%a = b*2
    end subroutine my_eq
    
    logical function my_unnary(a,b)
        type(my_type), intent(in) :: a,b
        
        my_unnary = a%a < b%a
    end function my_unnary


    elemental integer function func_elem_int(x)
        integer,intent(in) :: x

        func_elem_int = x*2

    end function func_elem_int
    
    elemental real function func_elem_real(x)
        real, intent(in) :: x

        func_elem_real = x*2

    end function func_elem_real

    elemental real(dp) function func_elem_real_dp(x)
        real(dp), intent(in) :: x

        func_elem_real_dp = x*2

    end function func_elem_real_dp


    subroutine test(x)
        integer :: x,i
        integer, allocatable,dimension(:) :: xarr,yarr
    
    
        write(*,*) func_elem_int(1)
        write(*,*) func_elem_int((/1,2,3,4,5/))
    
        allocate(xarr(x),yarr(x))
        
        do i=1,x
            xarr(i) = i**2
        end do
        
        yarr = func_elem_int(xarr)
    
    end subroutine test



    integer function convert_int(x)
        integer, intent(in) :: x
        convert_int = x * 5
    end function convert_int

    real function convert_real(x)
        real, intent(in) :: x
        convert_real = x * 5
    end function convert_real
    
    real(dp) function convert_real_dp(x)
        real(dp), intent(in) :: x
        convert_real_dp = x * 5
    end function convert_real_dp
    
    character(len=5) function convert_str(x)
        character(len=1), intent(in) :: x
        character(len=1) :: tmp
        integer :: i
        do i=0,5
            write(tmp,*) x
            convert_str(i:i) = tmp
        end do
    end function convert_str
    
    integer function convert_cmplx(x)
        complex, intent(in) :: x
        convert_cmplx = x * 5
    end function convert_cmplx


    function func_str_int_len(i) result(s)
        ! Github issue #12
        integer, intent(in) :: i
        character(len=str_int_len(i)) :: s
        write(s, '(i0)') i
    end function func_str_int_len
          
    pure integer function str_int_len(i) result(sz)
        ! Returns the length of the string representation of 'i'
        integer, intent(in) :: i
        integer, parameter :: MAX_STR = 100
        character(MAX_STR) :: s
        ! If 's' is too short (MAX_STR too small), Fortran will abort with:
        ! "Fortran runtime error: End of record"
        write(s, '(i0)') i
        sz = len_trim(s)
    end function str_int_len


    function func_mesh_exp(N) result(mesh)
        ! Github issues #13
        integer, intent(in) :: N
        integer(dp) :: mesh(N+1)
        integer :: i
        
        do i=1,n+1
            mesh(i) = i
        end do
        
    end function func_mesh_exp


    subroutine func_mesh_exp2(x,N) 
        integer, intent(in) :: N
        integer :: x(N+1)
        integer :: i
        
        do i=1,n+1
            x(i) = i
        end do
        
    end subroutine func_mesh_exp2


    subroutine func_mesh_exp3(x,N) 
        integer, intent(in) :: N
        integer :: x((N*2)+1)
        integer :: i
        
        do i=1,(N*2)+1
            x(i) = i
        end do
        
    end subroutine func_mesh_exp3


    subroutine func_mesh_exp4(x,N) 
        integer, intent(in) :: N
        integer :: x((N+3)*2+1)
        integer :: i
        
        do i=1,(N+3)*2+1
            x(i) = i
        end do
        
    end subroutine func_mesh_exp4

    subroutine check_exp_2d_2m3_nt(arr, NT, success)
        ! Github issues #19
        integer, intent(in) :: NT
        integer, dimension(3,NT) :: arr
        logical :: success
        
        success=.false.
    
        
        arr(1,NT) = 5

    end subroutine check_exp_2d_2m3_nt
    
end module face
