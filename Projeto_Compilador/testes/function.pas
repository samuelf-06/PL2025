program TesteFuncoes;

function dobro(x: integer): integer;
begin
  dobro := 2 * x;
end;

var
  resultado: integer;

begin
  resultado := dobro(7);
  writeln('O dobro de 7 é: ', resultado);
end.
