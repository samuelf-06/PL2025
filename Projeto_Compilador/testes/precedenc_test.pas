program precedence_test;
var 
    a, b, c, d, e: integer;
begin
    a := 3 + 4 * 5;
    b := (3 + 4) * 5;
    c := 10 - 2 - 1;
    d := 2 + 3 * 4 - 5;
    e := a + b * c > d - e;

    writeln('a = ', a);
    writeln('b = ', b);
    writeln('c = ', c);
    writeln('d = ', d);
    writeln('e = ', e);
end.
