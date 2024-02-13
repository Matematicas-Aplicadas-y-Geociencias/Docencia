%Rutina para reproducir señales 

a1=0.5; T1=10.1;   

fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=1024;%tiempo total en segundos
t=0:1/fm:endt;
ETA=a1.*cos((2*pi/T1).*t);

fm=0.3;%3 segundos
t1=1:1/fm:endt;
ETA1=a1.*cos((2*pi/T1).*t1);

fm=0.01666;%60 segundos
t2=1:1/fm:endt;
ETA2=a1.*cos((2*pi/T1).*t2);

figure
subplot(3,1,1)
plot(t,ETA)
axis([0 t(end) -0.7 0.7])
title('señal original')
subplot(3,1,2)
plot(t1,ETA1,'.r')
axis([0 t1(end) -0.7 0.7])
ylabel('amplitud')
hold off
grid
subplot(3,1,3)
plot(t2,ETA2,'.k')
axis([0 t2(end) -0.7 0.7])
ylabel('Solapado 2')
xlabel('tiempo (s)')


%agregar variaciones aleatorias
%distribución normal,(promedio=0,
%std=0.2, 1 columna, length(t) filas
%R=random('Normal',0,0.1,1,length(t));%solo funciona con Statistics and Machine Learning Toolbox 

%Generacion de numeros aleatorios
a = 0.1;%desviacion estandar
b = 0;%media
R = a.*randn(1,length(t)) + b;
plot(t,R)

ETAr=ETA+R;
subplot(3,1,1)
plot(t,ETA)
subplot(3,1,2)
plot(t,R)
subplot(3,1,3)
plot(t,ETAr)

%serie de tiempo con una tendencia
y=(2/(5*60))*t;
ETAB=(ETAr)+y;
hold on
plot(t,ETAB,'k')

NoEst=[t/n; ETAB];
dlmwrite('NoEst2.txt',NoEst);

%
