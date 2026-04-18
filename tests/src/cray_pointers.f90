! SPDX-License-Identifier: GPL-2.0+

module cray_ptrs

    use iso_fortran_env, only: output_unit, real128
    
    implicit none
   
    ! Cray pointers:
    real cray_target(10)
    real cray_pointee(10)
    pointer (ipt, cray_pointee)

    
    contains

end module cray_ptrs
