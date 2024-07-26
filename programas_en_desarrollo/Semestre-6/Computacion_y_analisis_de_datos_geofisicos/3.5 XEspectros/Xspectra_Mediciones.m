%Espectros cruzados de TKE y Catenatum
X=serie_tkeA;
Y=Ab_abs1hr;

N=length(X);
fm=24;
m=4096;%2048;%8192;%87512;%32768;%512;%,
n=m/2;
window=hanning(m);

[XSp01,F]=cpsd(X,Y,hanning(m),n,m,fm);
[Coh01,F]=mscohere(X,Y,hanning(m),n,m,fm);
XSp=sqrt(real(XSp01).^2+imag(XSp01).^2);%magnitud total del espectro cruzado


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

%Espectro cruzado con limites de confianza
s=find(Coh01-Clim>0);
Coh=zeros(length(Coh01));
Coh(s)=Coh01(s);
XSpec=XSp.*Coh;

figure
subplot(3,1,1)
semilogx(F,real(XSp01),'b')
hold on
semilogx(F,imag(XSp01),'r')
legend('Cxy','Qxy')
title(num2str(m))
title('co-espectro')
grid
subplot(3,1,2)
semilogx(F,Coh01)
hold on
semilogx(li,w,'r')
title('espectro de coherencia')
subplot(3,1,3)
semilogx(F,Ph01,'or')
title('espectro de fase')
grid


figure
subplot(2,1,1)
semilogx(F,XSpec,'b')
title('Espectro cruzado coherente')
grid
subplot(2,1,2)
semilogx(F,Ph01,'or')
title('espectro de fase')
grid

clear NOI ph Ph01 s t w window x X XSp01 y Y cl Clim Coh01 conf dof F fm li m n N 


