
module unicode
    implicit none

    integer,parameter :: CK = selected_char_kind('ISO_10646')

    character(kind=ck,len=100),parameter :: uni_param = ck_'😀😎😩'

    character(kind=ck,len=100) :: uni_set = ck_'😀😎😩'

    character(kind=ck,len=16),dimension(3),parameter :: uni_words = &
        [character(kind=ck,len=16) :: ck_'alpha', ck_'smile 😀', ck_'music 🎵']

    abstract interface
        function unicode_transform_iface(s) result(out)
            import ck
            character(kind=ck,len=*), intent(in) :: s
            character(kind=ck,len=:), allocatable :: out
        end function unicode_transform_iface
    end interface

contains

    subroutine set_unicode_scalar(dst, src)
        character(kind=ck,len=*), intent(out) :: dst
        character(kind=ck,len=*), intent(in) :: src

        dst = src
    end subroutine set_unicode_scalar

    function unicode_join(lhs, rhs) result(res)
        character(kind=ck,len=*), intent(in) :: lhs
        character(kind=ck,len=*), intent(in) :: rhs
        character(kind=ck,len=:), allocatable :: res

        res = lhs // rhs
    end function unicode_join

    function unicode_pick(arr, idx) result(res)
        character(kind=ck,len=*), intent(in) :: arr(:)
        integer, intent(in) :: idx
        character(kind=ck,len=len(arr(1))) :: res

        res = arr(idx)
    end function unicode_pick

    subroutine copy_unicode_array(src, dst)
        character(kind=ck,len=*), intent(in) :: src(:)
        character(kind=ck,len=*), intent(out) :: dst(:)

        dst = src
    end subroutine copy_unicode_array

    subroutine add_suffix_inplace(arr, suffix)
        character(kind=ck,len=*), intent(inout) :: arr(:)
        character(kind=ck,len=*), intent(in) :: suffix
        integer :: i

        do i = 1, size(arr)
            arr(i) = trim(arr(i)) // suffix
        end do
    end subroutine add_suffix_inplace

    function unicode_with_suffix(arr, suffix) result(out)
        character(kind=ck,len=*), intent(in) :: arr(:)
        character(kind=ck,len=*), intent(in) :: suffix
        character(kind=ck,len=:), allocatable :: out(:)
        integer :: i

        allocate(character(kind=ck,len=len(arr(1)) + len(suffix)) :: out(size(arr)))
        do i = 1, size(arr)
            out(i) = trim(arr(i)) // suffix
        end do
    end function unicode_with_suffix

    subroutine apply_unicode_transform(arr, fn, out)
        character(kind=ck,len=*), intent(in) :: arr(:)
        procedure(unicode_transform_iface) :: fn
        character(kind=ck,len=:), allocatable, intent(out) :: out(:)
        integer :: i

        allocate(character(kind=ck,len=len(arr(1))) :: out(size(arr)))
        do i = 1, size(arr)
            out(i) = fn(arr(i))
        end do
    end subroutine apply_unicode_transform

    subroutine copy_unicode_assumed_rank(src, dst)
        character(kind=ck,len=*), intent(in) :: src(..)
        character(kind=ck,len=*), intent(out) :: dst(..)

        select rank (src)
        rank (1)
            select rank (dst)
            rank (1)
                dst = src
            end select
        rank (2)
            select rank (dst)
            rank (2)
                dst = src
            end select
        end select
    end subroutine copy_unicode_assumed_rank

end module unicode