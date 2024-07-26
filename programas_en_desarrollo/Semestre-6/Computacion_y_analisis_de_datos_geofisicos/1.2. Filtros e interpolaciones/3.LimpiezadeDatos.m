%Comenzamos a limpiar datos y procesarlos...
%1. visualizar los datos 
%Graficar una señal en cada eje
yyaxis('left')
plot(time,cond,'.')
yyaxis('right')
plot(time,p,'.')
datetick
%plot(time,t,'.')

figure
scatter(time,p,30,cond,'filled')
datetick
colorbar

%2. Acotar los datos en tiempo...graficar solo los datos crudos de conductividad para visualizar mejor el
%el indice de datos a eliminar.
plot(cond,'.r')

%Escoger con el cursor el principio y fin donde queremos cortar exportando
%los indices al espacio de trabajo.
cond2=cond(cursor_info1.DataIndex:cursor_info2.DataIndex);
time2=time(cursor_info1.DataIndex:cursor_info2.DataIndex);
t2=t(cursor_info1.DataIndex:cursor_info2.DataIndex);
p2=p(cursor_info1.DataIndex:cursor_info2.DataIndex);

plot(p2,'.')

%3. Acotar los datos en magnitudes y determinar tendencias basado en la presión. 
s=find(p2>=41);
cond3=cond2(s);
time3=time2(s);
plot(time,cond,'.')
hold on
plot(time3,cond3,'.r')
datetick

plot(cond3,'.r')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%4. Los datos ruidosos pueden ser filtrados utilizando un filtro de media
%movil que està en la funcion:
cond4=smoothdata(cond3,'movmean',200);%donde 200 es el tamaño de la ventana
%puedes intentar tambièn utilizar otros mètodos de suavizado como ,'rloess';'movmean'
%Luego verificas su funcionamiento graficando....
hold on; plot(cond4,'k')
%%PROGRAMA TU PROPIA RUTINA DE MEDIA MOVIL.

%5.Segunda iteraciòn de limpeza
%Utilizar la señal filtrada para hacer una refinaciòn en los filtros
cond5=cond4-1;%reducir valores para no cortar datos buenos
plot(cond5,'b')

crit1=cond3-cond5;%Criterio para filtrar(que por cierto elimina tambien tendencias). 
plot(crit1,'.')
s2=find(crit1>0);

%Eliminar datos en segunda ronda
cond6=cond3(s2);
time6=time3(s2);
%volver a utilizar el filtro smooth
cond7=smoothdata(cond6,'movmean',200);%donde 200 es el tamaño de la ventana
plot(cond6,'.r');hold on;plot(cond7,'k')
cond8=smoothdata(cond6,'movmean',100);%donde 200 es el tamaño de la ventana
plot(cond8,'b')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%RESUMEN DE LO LOGRADO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plot(time,cond,'.k'); hold on; plot(time3,cond3,'.b'); plot(time6,cond7,'.r')
datetick

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Como rellenar huecos en series de datos: 
%Interpolaciòn lineal ejemplo simple - principios bàsicos
x=0:0.5:10;
m=0.5;
y=m.*x;

plot(x,y)
grid

y1=0.5;y2=3.5;x1=1;x2=7;
x=5;
y=y1+((x-x1)/(x2-x1))*(y2-y1);

%función de MATLAB para interpolar
cond9=interp1(time6,cond7,time2);%el método lineal es el pre-establecido, 
%intenta el método spline ,'spline' que emula mejor el comportamiento de los datos
plot(time2,cond9,'.c')











%Abajo hice lo mismo para la señal de presiòn
p2=p(cursor_info1.DataIndex:cursor_info2.DataIndex);
plot(time2,p2,'.')
hold on
plot(time2(s),p2(s),'.r')
datetick
p3=smoothdata(p2(s),'movmean',200);
hold on
plot(time2(s),p3,'.b')
datetick

scatter(time2(s),p3,30,cond3,'filled')
datetick
colorbar

      

             


        


