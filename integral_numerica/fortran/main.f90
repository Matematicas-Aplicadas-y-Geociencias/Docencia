program main
    use moduloIntegralNumerica
    implicit none
    real(8) :: a = 0, b = 1
    real(8) :: valorIntegral
    integer :: n = 160

    ! call midpointRule(a, b, n, valorIntegral)
    ! call trapezoidalRule(a, b, n, valorIntegral)
    call simpsonRule(a, b, n, valorIntegral)

    print '(A, F18.14)', 'El valor aproximado de la integral es: ', valorIntegral

end program main
