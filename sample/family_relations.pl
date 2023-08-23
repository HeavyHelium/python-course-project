parent(hamish, john).
parent(john, rosie).
parent(rosie, jack).

parent(mary, rosie).
parent(mary, anne).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).


sibling(X, Y) :- parent(Z, X), parent(Z, Y), not(is(X, Y)).

is(X, X).
