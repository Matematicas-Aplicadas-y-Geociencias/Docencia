%Señal sinusoidal
a1=1; T1=10;  
a2=0.5; T2=5; 
a3=0.3; T3=50;   

fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=1024;
t=0:1/fm:endt-(1/fm);

%Generacion de numeros aleatorios
a = 1.3;%desviacion estandar
b = 0;%media
R = a.*randn(1,length(t)) + b;

X1=a1.*cos((2*pi/T1).*t)+a2.*cos((2*pi/T2).*t)+a3.*cos((2*pi/T3).*t);
X=X1+R;%TempOcean;%NivelMar;%X1+R;%
%X=R;% NivelMar;% ;% ;Cyy;%
figure
plot(t,X,'.-')
hold on
plot(t,X1,'r')
axis([0 t(end) -2 2])

fm=48;
N=length(X);
n=1:N;
Ny=fm/2;%Frecuencia de Nyquist (máxima frecuencia a resolver)

ts=1/fm;%periodo de muestreo (tiempo)
freq1=(1:(N/2-1))/(N*ts);
f=[freq1, Ny,-Ny, -1.*fliplr(freq1)]';

for p=1:N-1
    arg=cos(((2*pi*p)./N).*n);
    A(p)=2/N.*sum(X.*arg);
    B(p)=2/N.*sum(X.*sin(((2*pi*p)./N).*n));
end
C=sqrt(A.^2+B.^2);
%vector de frecuencias


figure
plot(f,C,'r')
xlabel('frequency (cpd)')


clear A B C N Ny f freq1 fs n p ts