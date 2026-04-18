! SPDX-License-Identifier: GPL-2.0+

module isoc

    use iso_fortran_env, only: output_unit, real128
    use iso_c_binding
    
    implicit none
    
    ! Parameters
    integer, parameter :: dp = selected_real_kind(p=15)
    integer, parameter :: qp = selected_real_kind(p=30)
    integer, parameter :: lp = selected_int_kind(16)
    

    integer, bind(C,name='a_int_bind_c') :: a_int = 1
    integer(C_INT) :: a_c_int
    
    contains


    integer function func_bind_c(x) bind(C,name='c_bind_func')
        integer, intent(in) :: x
        func_bind_c = 2*x

    end function func_bind_c

    function c_inc_i32(x) result(y) bind(C, name='c_inc_i32')
        integer(C_INT), value, intent(in) :: x
        integer(C_INT) :: y

        y = x + 1_C_INT
    end function c_inc_i32

    function c_scale_f64(x, alpha) result(y) bind(C, name='c_scale_f64')
        real(C_DOUBLE), value, intent(in) :: x
        real(C_DOUBLE), value, intent(in) :: alpha
        real(C_DOUBLE) :: y

        y = x * alpha
    end function c_scale_f64

    function c_identity_ptr(p) result(outp) bind(C, name='c_identity_ptr')
        type(C_PTR), value, intent(in) :: p
        type(C_PTR) :: outp

        outp = p
    end function c_identity_ptr

    subroutine c_add_i32_arrays(a, b, c, n) bind(C, name='c_add_i32_arrays')
        integer(C_INT), intent(in) :: a(*)
        integer(C_INT), intent(in) :: b(*)
        integer(C_INT), intent(out) :: c(*)
        integer(C_INT), value, intent(in) :: n
        integer(C_INT) :: i

        do i = 1_C_INT, n
            c(i) = a(i) + b(i)
        end do
    end subroutine c_add_i32_arrays

    subroutine c_scale_f64_array(arr, n, alpha) bind(C, name='c_scale_f64_array')
        real(C_DOUBLE), intent(inout) :: arr(*)
        integer(C_INT), value, intent(in) :: n
        real(C_DOUBLE), value, intent(in) :: alpha
        integer(C_INT) :: i

        do i = 1_C_INT, n
            arr(i) = alpha * arr(i)
        end do
    end subroutine c_scale_f64_array

    subroutine c_split_complex(z, r, im, n) bind(C, name='c_split_complex')
        complex(C_DOUBLE_COMPLEX), intent(in) :: z(*)
        real(C_DOUBLE), intent(out) :: r(*)
        real(C_DOUBLE), intent(out) :: im(*)
        integer(C_INT), value, intent(in) :: n
        integer(C_INT) :: i

        do i = 1_C_INT, n
            r(i) = real(z(i), kind=C_DOUBLE)
            im(i) = aimag(z(i))
        end do
    end subroutine c_split_complex

    subroutine c_bool_not(inp, outp) bind(C, name='c_bool_not')
        logical(C_BOOL), value, intent(in) :: inp
        logical(C_BOOL), intent(out) :: outp

        outp = .not. inp
    end subroutine c_bool_not


end module isoc
