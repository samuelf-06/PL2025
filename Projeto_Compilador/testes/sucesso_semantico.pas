program SucessoSemantico;

function Soma(a, b: integer): integer;
begin
    Soma := a + b;
end;

var x, y: integer;

begin
    x := 5;
    y := Soma(x, 10);
    writeln('Resultado: ', y);
end.
