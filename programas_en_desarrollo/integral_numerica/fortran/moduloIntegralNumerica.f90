module moduloIntegralNumerica
    implicit none

contains
    subroutine midpointRule(a, b, n, valorIntegral)
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: a, b
        real(8), intent(out) :: valorIntegral

        integer i
        real(8) :: delta, h, hd2, point, midpoint
        real(8), dimension(n) :: imagenFuncion

        ! ****************************************************************************
        delta = b - a
        h = delta / n
        hd2 = h / 2

        do i = 1, n
            point = a + (i-1) * h
            midpoint = point + hd2
            imagenFuncion(i) = fun(midpoint)
        end do

        valorIntegral = h * sum(imagenFuncion)
    end subroutine midpointRule

    subroutine trapezoidalRule(a, b, n, valorIntegral)
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: a, b
        real(8), intent(out) :: valorIntegral

        integer i
        real(8) :: delta, h, hd2, point
        real(8), dimension(n+1) :: imagenFuncion

        ! ****************************************************************************
        delta = b - a
        h = delta / n
        hd2 = h / 2

        do i = 1, n+1
            point = a + (i-1) * h
            imagenFuncion(i) = fun(point)
        end do

        valorIntegral = hd2 * (imagenFuncion(1) + imagenFuncion(n+1) + 2 * sum(imagenFuncion(2:n)))
    end subroutine trapezoidalRule

    subroutine simpsonRule(a, b, n, valorIntegral)
        implicit none
        integer, intent(in) :: n
        real(8), intent(in) :: a, b
        real(8), intent(out) :: valorIntegral

        integer i
        real(8) :: delta, h, hd3, point
        real(8), dimension(n+1) :: imagenFuncion

        ! ****************************************************************************

        if (mod(n, 2) /= 0) then
            print *, 'El valor n = ', n, ', es impar y debe ser par.'
            valorIntegral = 0.
            return
        end if

        delta = b - a
        h = delta / n
        hd3 = h / 3

        do i = 1, n+1
            point = a + (i-1) * h
            imagenFuncion(i) = fun(point)
        end do

        valorIntegral = hd3 * (imagenFuncion(1) + imagenFuncion(n+1) + &
        4 * sum(imagenFuncion(2:n:2)) + 2 * sum(imagenFuncion(3:n-1:2)))

    end subroutine simpsonRule

    function fun(valorEntrada) result(valorSalida)
        real(8), intent(in) :: valorEntrada
        real(8) :: valorSalida

        valorSalida = exp(3*valorEntrada)

    end function fun

end module moduloIntegralNumerica
