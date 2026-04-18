! SPDX-License-Identifier: GPL-2.0+

module pdt

    use iso_fortran_env, only: output_unit

    implicit none

    ! Parameters
    integer, parameter :: sp = selected_real_kind(p=8)
    integer, parameter :: dp = selected_real_kind(p=15)
    integer, parameter :: qp = selected_real_kind(p=30)
    integer, parameter :: lp = selected_int_kind(16)

    type pdt_def(k, a)
        integer, kind :: k
        integer, len  :: a
        real(k)       :: array(a, a)
    end type pdt_def

    ! Module variables with different PDT instantiations.
    type(pdt_def(dp, 3)) :: pdt_dp_3
    type(pdt_def(sp, 3)) :: pdt_sp_3
    type(pdt_def(qp, 2)) :: pdt_qp_2

contains

    subroutine sub_write_pdt()
        write(output_unit, *) pdt_dp_3%array
    end subroutine sub_write_pdt

    subroutine set_module_values()
        pdt_dp_3%array = reshape([ &
            1.0_dp, 0.0_dp, 0.0_dp, &
            0.0_dp, 1.0_dp, 0.0_dp, &
            0.0_dp, 0.0_dp, 1.0_dp], shape(pdt_dp_3%array))

        pdt_sp_3%array = 2.0_sp
        pdt_qp_2%array = 3.0_qp
    end subroutine set_module_values

    ! INTENT(IN): reads PDT argument only.
    subroutine consume_pdt_in(x)
        type(pdt_def(dp, 3)), intent(in) :: x

        write(output_unit, '(a,f8.3)') 'trace(in)=', trace_dp3(x)
    end subroutine consume_pdt_in

    ! INTENT(OUT): initializes PDT argument.
    subroutine build_pdt_out(x, diag)
        type(pdt_def(dp, 3)), intent(out) :: x
        real(dp), intent(in)               :: diag

        x%array = 0.0_dp
        x%array(1, 1) = diag
        x%array(2, 2) = diag
        x%array(3, 3) = diag
    end subroutine build_pdt_out

    ! INTENT(INOUT): mutates PDT argument in place.
    subroutine scale_pdt_inout(x, factor)
        type(pdt_def(dp, 3)), intent(inout) :: x
        real(dp), intent(in)                :: factor

        x%array = x%array * factor
    end subroutine scale_pdt_inout

    ! Function returning a PDT instance.
    function make_identity_dp3(diag) result(x)
        real(dp), intent(in) :: diag
        type(pdt_def(dp, 3)) :: x

        call build_pdt_out(x, diag)
    end function make_identity_dp3

    ! Same pattern with different PDT kind parameter.
    function make_identity_sp3(diag) result(x)
        real(sp), intent(in) :: diag
        type(pdt_def(sp, 3)) :: x

        x%array = 0.0_sp
        x%array(1, 1) = diag
        x%array(2, 2) = diag
        x%array(3, 3) = diag
    end function make_identity_sp3

    ! Function returning a scalar derived from a PDT argument.
    function trace_dp3(x) result(t)
        type(pdt_def(dp, 3)), intent(in) :: x
        real(dp)                         :: t

        t = x%array(1, 1) + x%array(2, 2) + x%array(3, 3)
    end function trace_dp3

    ! Function taking PDT input and returning PDT output.
    function shifted_copy_dp3(x, offset) result(y)
        type(pdt_def(dp, 3)), intent(in) :: x
        real(dp), intent(in)             :: offset
        type(pdt_def(dp, 3))             :: y

        y%array = x%array
        y%array(1, 1) = y%array(1, 1) + offset
        y%array(2, 2) = y%array(2, 2) + offset
        y%array(3, 3) = y%array(3, 3) + offset
    end function shifted_copy_dp3

    subroutine sub_pdt()
        type(pdt_def(lp, 5)) :: x

        x%array = 2

        call set_module_values()
        call consume_pdt_in(pdt_dp_3)
        call build_pdt_out(pdt_dp_3, 4.0_dp)
        call scale_pdt_inout(pdt_dp_3, 0.5_dp)
        pdt_dp_3 = shifted_copy_dp3(pdt_dp_3, 1.0_dp)

        pdt_sp_3 = make_identity_sp3(2.0_sp)
        pdt_dp_3 = make_identity_dp3(3.0_dp)
    end subroutine sub_pdt

end module pdt
