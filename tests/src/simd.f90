! SPDX-License-Identifier: GPL-2.0+

module simd_ops

	use iso_fortran_env, only: real64
	use omp_lib, only: omp_get_max_threads, omp_set_num_threads, omp_get_thread_num

	implicit none

contains

	subroutine set_threads(nthreads)
		integer, intent(in) :: nthreads

		if (nthreads > 0) then
			call omp_set_num_threads(nthreads)
		end if
	end subroutine set_threads

	function max_threads() result(n)
		integer :: n

		n = omp_get_max_threads()
	end function max_threads

	subroutine saxpy_simd(alpha, x, y)
		real(real64), intent(in) :: alpha
		real(real64), intent(in) :: x(:)
		real(real64), intent(inout) :: y(:)
		integer :: i

		!$omp parallel do simd default(none) private(i) shared(alpha, x, y)
		do i = 1, size(x)
			y(i) = alpha * x(i) + y(i)
		end do
		!$omp end parallel do simd
	end subroutine saxpy_simd

	function dot_product_simd(x, y) result(dot)
		real(real64), intent(in) :: x(:)
		real(real64), intent(in) :: y(:)
		real(real64) :: dot
		integer :: i

		dot = 0.0_real64
		!$omp simd reduction(+:dot)
		do i = 1, size(x)
			dot = dot + x(i) * y(i)
		end do
		!$omp end simd
	end function dot_product_simd

	subroutine sections_example(a, b, c)
		real(real64), intent(inout) :: a(:)
		real(real64), intent(inout) :: b(:)
		real(real64), intent(out) :: c(:)

		!$omp parallel sections default(none) shared(a, b, c)
		!$omp section
		c = a + b
		!$omp section
		a = 2.0_real64 * a
		!$omp section
		b = b - 1.0_real64
		!$omp end parallel sections
	end subroutine sections_example

	subroutine reduction_schedule_example(x, sum_out, max_out)
		real(real64), intent(in) :: x(:)
		real(real64), intent(out) :: sum_out
		real(real64), intent(out) :: max_out
		integer :: i

		sum_out = 0.0_real64
		max_out = -huge(0.0_real64)
		!$omp parallel do default(none) private(i) shared(x) reduction(+:sum_out) reduction(max:max_out) schedule(dynamic, 4)
		do i = 1, size(x)
			sum_out = sum_out + x(i)
			max_out = max(max_out, x(i))
		end do
		!$omp end parallel do
	end subroutine reduction_schedule_example

	subroutine atomic_increment(counter, niters)
		integer, intent(inout) :: counter
		integer, intent(in) :: niters
		integer :: i

		!$omp parallel do default(none) private(i) shared(counter, niters)
		do i = 1, niters
			!$omp atomic update
			counter = counter + 1
		end do
		!$omp end parallel do
	end subroutine atomic_increment

	subroutine critical_min_example(x, global_min)
		real(real64), intent(in) :: x(:)
		real(real64), intent(out) :: global_min
		real(real64) :: local_min
		integer :: i

		global_min = huge(0.0_real64)
		!$omp parallel default(none) private(i, local_min) shared(x, global_min)
		local_min = huge(0.0_real64)
		!$omp do
		do i = 1, size(x)
			local_min = min(local_min, x(i))
		end do
		!$omp end do
		!$omp critical(min_update)
		global_min = min(global_min, local_min)
		!$omp end critical(min_update)
		!$omp end parallel
	end subroutine critical_min_example

	subroutine task_example(x, y)
		real(real64), intent(inout) :: x(:)
		real(real64), intent(inout) :: y(:)

		!$omp parallel default(none) shared(x, y)
		!$omp single
		!$omp task shared(x)
		call scale_array(x, 2.0_real64)
		!$omp end task
		!$omp task shared(y)
		call scale_array(y, 3.0_real64)
		!$omp end task
		!$omp taskwait
		!$omp end single
		!$omp end parallel
	end subroutine task_example

	subroutine single_master_example(single_tid, master_tid)
		integer, intent(out) :: single_tid
		integer, intent(out) :: master_tid

		single_tid = -1
		master_tid = -1
		!$omp parallel default(none) shared(single_tid, master_tid)
		!$omp single
		single_tid = omp_get_thread_num()
		!$omp end single
		!$omp master
		master_tid = omp_get_thread_num()
		!$omp end master
		!$omp end parallel
	end subroutine single_master_example

	subroutine collapse_2d_example(a, b, c)
		real(real64), intent(in) :: a(:, :)
		real(real64), intent(in) :: b(:, :)
		real(real64), intent(out) :: c(:, :)
		integer :: i, j

		!$omp parallel do collapse(2) default(none) private(i, j) shared(a, b, c)
		do j = 1, size(a, 2)
			do i = 1, size(a, 1)
				c(i, j) = a(i, j) + b(i, j)
			end do
		end do
		!$omp end parallel do
	end subroutine collapse_2d_example

	subroutine scale_array(a, factor)
		real(real64), intent(inout) :: a(:)
		real(real64), intent(in) :: factor
		integer :: i

		do i = 1, size(a)
			a(i) = factor * a(i)
		end do
	end subroutine scale_array

end module simd_ops
