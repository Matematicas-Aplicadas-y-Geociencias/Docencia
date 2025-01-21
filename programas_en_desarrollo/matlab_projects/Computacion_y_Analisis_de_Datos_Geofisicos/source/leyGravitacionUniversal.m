function F = leyGravitacionUniversal(masa1, masa2, radio)
    G = 6.67392e-11;
    F = G * masa1 * masa2 / radio^2;
end