program Quadrado;

function quadrado(x: integer): integer;
begin
  quadrado := x * x;
end;

var
  res: integer;
begin
  res := quadrado(5);
  writeln('Quadrado de 5 é: ', res);
end.
