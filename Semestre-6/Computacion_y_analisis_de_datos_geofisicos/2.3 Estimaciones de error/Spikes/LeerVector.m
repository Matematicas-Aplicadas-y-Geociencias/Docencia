%%Archivos del velocimetro VECTOR
    dat=dlmread('Sarg0401_1.dat');
    v=dat(:,4);%Velocidad X
    h=dat(:,15);%profundidad
    clear dat
    
%Limpiar datos para acotar en tiempo y usar solo los datos que estan ene le agua
subplot(2,1,1)
plot(h)
title('presión')
subplot(2,1,2)
plot(v,'.')
hold on
plot(v2)
title('velocidad')

%Escoger los limites para acotar en tiempo
a=cursor_info1.DataIndex; b=length(h);
v=v(a:b); h=h(a:b);N=length(v);

Vmean=mean(v);%Velocidad Y (N-S en el contexto de Gorgos)
Hmean=mean(h);%profundidad promedio para cada burst
vfluc=v-Vmean;
vsd=std(vfluc);

%definimos un vector tiempo para graficar si es necesario
tsec=1/8:1/8:(N/8);

%aplicamos criterio visual de 3std
crit1=[tsec(1) tsec(end)];
crit2=[3*vsd 3*vsd];
plot(tsec,v,'.')%ver comportamiento de abs(v)
hold on
plot(crit1,crit2,crit1,-crit2,'r')

s=find(v<3*vsd & v>-3*vsd);
s=find(abs(v)<3*vsd); 
%verificamos si logramos separar la señal
plot(tsec(s),v(s),'.r')

%ahora rellenamos huecos con una interpolacion cubica
v2=interp1(tsec(s),v(s),tsec,'pchip');
plot(tsec,v2,'c')

