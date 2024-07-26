%Espectros para una señal medida de temperatura y nivel del mar
%cargar los datos de Telchac.mat
x=x1';%debe ser vector columna
t=t;
X=detrend(x,0);%
s=2^16; %preferencia un multiplo de 2^n
X(end+1:s)=0;

%visualizar datos previo al análisis
plot(X)

N=length(X);
fm=48;

%Hacer el espectro de la señal generada, para determinar el valle
%hacerlo con pwelch...usar la rutina de Welch...

valley=0.5625;%valle para separacion de altas y bajas frecuencias
Ny=fm/2;%frecuencia de Nyquist
tm=1/fm;%periodo de muestreo como la inversa de la frecuencia de muestreo

%Calcular la Transformada Rápida de Fourier (fft)...aqui recordar como
%funciona esta fft con Recuerda_TransformadaFourier.m
fft1=fft(X);

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

N2=length(x);
lpdata=real(ifft(lpfft));
lpdata=lpdata(1:N2);
hpdata=real(ifft(hpfft));
hpdata=hpdata(1:N2);

%graficar resultado del filtro Fourier
a=0.2;
figure
subplot(3,1,1)
plot(t,x)
axis([t(1) t(end) -a a])
datetick
grid

subplot(3,1,2)
plot(t,hpdata,'r')
axis([t(1) t(end) -a a])
datetick
grid

subplot(3,1,3)
plot(t,lpdata)
axis([t(1) t(end) -a a])
datetick
grid


