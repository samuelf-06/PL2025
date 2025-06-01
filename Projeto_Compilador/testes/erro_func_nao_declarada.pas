program TesteFuncNaoDeclarada;
var x: integer;
begin
    x := Soma(5, 10);  { 'Soma' não está declarada → deve dar erro }
end.
