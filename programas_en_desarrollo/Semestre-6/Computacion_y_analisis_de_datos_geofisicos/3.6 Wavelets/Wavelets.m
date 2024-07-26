a1=0.5; T1=5;e1=0;       
a2=1;  T2=10; e2=0;
a3=0.25;T3=100;e3=0;

fm=4;
endt=1024;
t=0:1/fm:endt-(1/fm);

ETA1=a1.*cos((2*pi/T1).*t+e1);
ETA2=a2.*cos((2*pi/T2).*t+e2);
ETA3=a3.*cos((2*pi/T3).*t+e3);

ETA=ETA1+ETA2+ETA3;

subplot(4,1,1)
plot(t,ETA1)
%axis([0 endt/24 -2.5 2.5])
title('5')
subplot(4,1,2)
plot(t,ETA2)
%axis([0 endt/24 -2.5 2.5])
ylabel('amplitude')
title('15')
subplot(4,1,3)
plot(t,ETA3)
%axis([0 endt/24 -2.5 2.5])
title('100')
subplot(4,1,4)
plot(t,ETA)
%axis([0 endt/24 -2.5 2.5])
xlabel('segundos')
title('suma')
clear T1 T2 T3 a1 a2 a3 e1 e2 e3 endt

clear a1 a2 a3 T1 T2 T3 e1 e2 e3 endt ETA1 ETA2 ETA3

[wt,f,coi] = cwt(ETA,'amor',fm);%señal y la frecuencia de muestreo
magnitud=sqrt(real(wt).^2+imag(wt).^2);
figure
pcolor(t,f,magnitud); shading flat%eje y en log
ax=gca;
ax.YScale = 'log';
colorbar
hold on
plot(t,coi,'w')

WavSpec=sum(magnitud');
figure
loglog(f,WavSpec)


%Serie de tiempo fuertemente no estacionaria
fm = 1000;
t = 0:1/fm:1;
x = cos(2*pi*32*t).*(t>=0.1 & t<0.3) + sin(2*pi*64*t).*(t>0.7);
plot(t,x)
%Agregar ruido Gaussiano con desv.standard=0.5.
a = 0.5;%desviacion estandar
b = 0;%media
R = a.*randn(1,length(t)) + b;

x2 = x + R;
plot(t,x2)

%obtener el gráfico de cwt con una Morlet wavelet.
[wt,f,coi] = cwt(x,'amor',fm);%señal y la frecuencia de muestreo
magnitud=sqrt(real(wt).^2+imag(wt).^2);
figure
pcolor(t,f,magnitud); shading flat%eje y en log
colorbar
hold on
plot(t,coi,'w')
%datetick




