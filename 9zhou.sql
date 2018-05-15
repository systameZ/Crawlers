declare
v_sum int:=0;
begin
for i in 1..100 loop
if i%2!=0 then
v_um:=v_sum+i;
end if;
end loop;
end;

begin
for i in 1..9 loop
 for j in 1..i loop
  dbms_output.put(to_char(j)||'*'||to_char(i)||'='||to_char(i*j)||'  ');
 end loop;
 dbms_output.put_line('');
 end loop;
 end;
 
 declare
 v_sum int:=1;
 begin
 for i in 1..10 loop
     v_sum:=i*v_sum;
 end loop;
 dbms_output.put_line(v_sum);
 end;
 
 begin
 for i in 2..9 loop
     dbms_output.put_line(rapd(to_char(i-1),i,'*'));
 end loop;
 end;
 
 
 
 
 
 
 
 
 
 
 
 