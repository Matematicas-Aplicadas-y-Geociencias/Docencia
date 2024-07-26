%Espectros para una señal medida de temperatura y nivel del mar
a1=0.5; T1=100;   
a2=0.25; T2=10; 
fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=1024;
t=0:1/fm:endt-(1/fm);

%Generacion de numeros aleatorios
 a3 = 0;%desviacion estandar
 b = 0;%media
 R = a3.*randn(1,length(t)) + b;
%Aqui generamos una señal estocástica que consta de una parte periodica y
%otra parte aleatoria
X1=a1.*cos((2*pi/T1).*t);X2=a2.*cos((2*pi/T2).*t);
X=X1+X2+R;%señal puramente periodica para ver la eficiencia del filtro

%Visualizar la función que generamos como sumatoria de periodos
a=1.25*(a1+a2+a3);
s=find(t==100*T2);
%graficos
subplot(2,1,1)
plot(t,X,'.-')
axis([0 t(s) -a a])
grid
subplot(2,1,2)
plot(t,X1,'.-r')
hold on
plot(t,X2,'.-k')
axis([0 t(s) -a a])
grid

%Hacer el espectro de la señal generada, para determinar el valle
%hacerlo con pwelch...usar la rutina de Welch...

valley=0.0625;%valle para separacion de altas y bajas frecuencias
y=X;
N=length(y);
Ny=fm/2;%frecuencia de Nyquist
tm=1/fm;%periodo de muestreo como la inversa de la frecuencia de muestreo

%Calcular la Transformada Rápida de Fourier (fft)...aqui recordar como
%funciona esta fft con Recuerda_TransformadaFourier.m
fft1=fft(y);

%genera el vector de frecuencias
if ceil(N/2)==N/2
freq1=(1:(N/2-1))/(N*tm);%esta es la mitad del vector de frecuencias
freq=[freq1, Ny,-Ny, -1.*fliplr(freq1)]';
else 
disp('length of fft not right');
end

%Generación de las ventanas para el filtrado
left0=zeros(size(freq1));
left1=ones(size(freq1));
%posiciones importantes
nt=(N/2)-1;
nv=round(((nt)*valley)/Ny); %esta es la posición donde se encuentra el valle en el vector de frecuencias
nh=4; %nh is the number of points in the hanning window - specifies width of hanning slope (width is nh/2)
nl=round(nv-(nh/4));%posición un valor antes del valle
nr=round(nv+(nh/4));%posición un valor despues del valle 
han=hanning(nh);
left(1:nl)=left0(1:nl);
left(nl+1:nr)=han(1:nh/2);
left(nr+1:nt)=left1(nr+1:nt);
right=fliplr(left);
highhan=[0,left,1,right];
lowhan=1-highhan;

%Visualizaciòn de todo el proceso
 figure
 plot(freq,highhan,'.-r')
 hold on
 plot(freq,abs(fft1)/max(abs(fft1)))
 plot(freq,lowhan,'.-k')
 axis([min(freq) max(freq) 0 1])

hpfft=highhan.*(fft1);
lpfft=lowhan.*(fft1);

lpdata=real(ifft(lpfft));
hpdata=real(ifft(hpfft));

%graficar resultado del filtro Fourier
a=1;
figure
subplot(3,1,1)
plot(t,y)
axis([t(1) t(end) -a a])
grid

subplot(3,1,2)
plot(t,hpdata,'r')
hold on
plot(t,X2,'.k')
axis([t(1) t(end) -a a])
grid

subplot(3,1,3)
plot(t,lpdata)
hold on
plot(t,X1,'.k')
axis([t(1) t(end) -a a])
grid

T=(hpdata+lpdata)-R;

figure
plot(X1+X2)
hold on
plot(T,'.')
