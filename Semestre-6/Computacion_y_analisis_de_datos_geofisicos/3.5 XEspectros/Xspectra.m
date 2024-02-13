%Generar dos señales ficticias
%primera señal


%Segunda señal
a1=0.3; T1=12;e1=0;   
a2=0.5; T2=300;e2=0;
a3=0.3; T3=200;e3=0;
X2=a1.*cos((2*pi/T1).*t)+a2.*cos((2*pi/T2).*t+e2)+a3.*cos((2*pi/T3).*t+e3);
clear a1 a2 a3 T1 T2 T3 e1 e2 e3 endt

%Generacion de numeros aleatorios
% a = 0.3;%desviacion estandar
% b = 0;%media
% R = a.*randn(1,length(t)) + b;
% X=X1+R;

figure
plot(t,X1)
hold on
plot(t,X2,'r')


N=length(X1);
m=2048;%8192;%87512;%32768;%512;%,4096;%
n=m/2;
window=hanning(m);

[XSp01,F]=cpsd(X1,X2,hanning(m),n,m,fm);
[Coh01,F]=mscohere(X1,X2,hanning(m),n,m,fm);

%Calculo de la fase entre las series de tiempo
ph=angle(XSp01);
%Convertir a grados de radianes
Ph01=ph.*(180./pi);

%limites de confianza para la coherencia
cl=0.95; 
NOI=N./m; %No. of non-overlapping intervals
dof=3.82.*NOI-3.24; %degrees of freedom if Hanning window is used
conf=1-cl; %At 95% confidence limit
Clim=1-conf.^(1/((0.5*dof)-1));
li=[F(2) F(end-1)]; %Confidence limit vectors
w=[Clim Clim];

figure
subplot(3,1,1)
semilogx(F,real(XSp01),'k')
hold on
semilogx(F,imag(XSp01),'r')
legend('Cxy','Qxy')
title(num2str(m))
title('co-espectro')
subplot(3,1,2)
semilogx(F,Coh01)
hold on
semilogx(li,w,'r')
title('espectro de coherencia')
subplot(3,1,3)
semilogx(F,Ph01,'or')
title('espectro de fase')




