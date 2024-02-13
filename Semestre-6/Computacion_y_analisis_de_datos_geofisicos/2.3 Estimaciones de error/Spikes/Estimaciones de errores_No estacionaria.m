%Como limpiar datos con el criterio de 3std cuando los datos tienen mucha
%variabilidad...cargar DatosChelem (arrastres de CTD)

%1. Acotar en tiempo...Escoger con el cursor el principio y fin donde queremos cortar exportando
%los indices al espacio de trabajo.
cond2=cond(cursor_info1.DataIndex:cursor_info2.DataIndex);
time2=time(cursor_info1.DataIndex:cursor_info2.DataIndex);
t2=t(cursor_info1.DataIndex:cursor_info2.DataIndex);
p2=p(cursor_info1.DataIndex:cursor_info2.DataIndex);



%2. Adoptar un criterio mas cuantitativo escogiendo solo los datos sumergidos
%utilizando un umbral en el sensor de presión. 
plot(p2,'.')%graficar para escoger criterio
s=find(p2>=1040);%Criterio
plot(time2,cond2,'.')
hold on
plot(time2(s),cond2(s),'.r')

%primer filtro de limpieza
cond3=cond2(s);
time3=time2(s);

%intentar ver que pasa si aplicamos la convención heuristica de 3std a los
%datos como están
Cmean=mean(cond3); 
Cfluc=cond3-Cmean;
Csd=std(Cfluc);
plot(time3,Cfluc,'.')
datetick

crit1=[time3(1) time3(end)];
crit2=[3*Csd 3*Csd];
hold on
plot(crit1,crit2,crit1,-crit2,'r')

%3std no funciona en datos que presentan tanta variación... que hacer

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%4. Aplicar filtro de media movil para remover la tendencia general:
cond4=smoothdata(cond3,'rloess',1000);
plot(time3,cond3,'.')
hold on; 
plot(time3,cond4,'k')

%5.Quitamos la tendencia general a los datos
cond5=cond3-cond4; 
plot(cond5,'.')
%6. Y a la nueva señal le aplicamos la convención heuristica de 3std
C5fluc=cond5-mean(cond5);
Csd5=std(C5fluc);
plot(time3,C5fluc,'.')
crit2=[3*Csd5 3*Csd5];
hold on
plot(crit1,crit2,crit1,-crit2,'r')
%Eliminar datos que se salen de 3sd
s2=find(C5fluc<3*Csd5 & C5fluc>-3*Csd5);
plot(time3(s2),C5fluc(s2),'.r')

%Definimos nuevo set de datos con los errores que sobrepasan 3std limpios
cond6=cond3(s2); 
time6=time3(s2);

plot(time2,cond2,'.')
hold on
plot(time6,cond6,'.r')
datetick

%volver a utilizar el filtro smooth en los nuevos datos
cond7=smoothdata(cond6,'rloess',120);
plot(time6,cond7,'.c');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Finalmente rellenamos huecos en la series de datos: 
cond8=interp1(time6,cond7,time2);%el método lineal es el pre-establecido, 
%intenta el método spline ,'spline' que emula mejor el comportamiento de los datos
plot(time2,cond8,'.m')











