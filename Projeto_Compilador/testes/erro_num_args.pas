program TesteNumArgs;

function Soma(a, b: integer): integer;
begin
    Soma := a + b;
end;

var x: integer;

begin
    x := Soma(5);  { Falta um argumento → erro }
end.
