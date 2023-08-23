parent(pesho, gosho).
parent(gosho, ana).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

slkdfkdfm.
