module coarrays
    implicit none
    integer :: status_flag[*]
    integer :: image_values(4)[*]
    integer, allocatable :: work(:)[:]
    integer, allocatable :: replicated(:)[:]

contains

    subroutine initialize_coarrays(n)
        integer, intent(in) :: n

        if (allocated(work)) deallocate(work)
        if (allocated(replicated)) deallocate(replicated)

        allocate(work(n)[*])
        allocate(replicated(2)[*])

        work = this_image()
        replicated = [this_image(), num_images()]
        status_flag = 1
        image_values = [this_image(), this_image() + 1, this_image() + 2, this_image() + 3]

        sync all
    end subroutine initialize_coarrays

    subroutine coindexed_write_example(target_image, value)
        integer, intent(in) :: target_image
        integer, intent(in) :: value

        if (target_image >= 1 .and. target_image <= num_images()) then
            status_flag[target_image] = value
            image_values(1)[target_image] = value
        end if
    end subroutine coindexed_write_example

    subroutine point_to_point_exchange(left_image, right_image)
        integer, intent(in) :: left_image
        integer, intent(in) :: right_image

        if (.not. allocated(work)) return

        if (left_image >= 1 .and. left_image <= num_images()) then
            work(1)[left_image] = this_image()
        end if

        if (right_image >= 1 .and. right_image <= num_images()) then
            work(size(work))[right_image] = this_image()
        end if

        sync images([left_image, right_image])
    end subroutine point_to_point_exchange

    subroutine gather_first_element(root_image, total)
        integer, intent(in) :: root_image
        integer, intent(out) :: total
        integer :: img

        total = 0
        if (.not. allocated(work)) return

        sync all
        if (this_image() == root_image) then
            do img = 1, num_images()
                total = total + work(1)[img]
            end do
        end if
        sync all
    end subroutine gather_first_element

    subroutine deallocate_coarrays()
        if (allocated(work)) deallocate(work)
        if (allocated(replicated)) deallocate(replicated)
        sync all
    end subroutine deallocate_coarrays

end module coarrays