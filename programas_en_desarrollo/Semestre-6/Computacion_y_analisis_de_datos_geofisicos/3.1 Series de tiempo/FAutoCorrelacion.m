%% Señal sinusoidal
a1=0.5; T1=10.1;%Simple
a2=1; T2=5;%Con un armonico dominante y luego chico
a3=1; T3=50;%Con una baja frecuencia
% endt=1024*10;

%Aqui generamos el vector de tiempo
fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=1024;
t=0:1/fm:endt;
%ETA=a1.*cos((2*pi/T1).*t);
ETA=a1.*cos((2*pi/T1).*t)+a2.*cos((2*pi/T2).*t)+a3.*cos((2*pi/T3).*t);
plot(t,ETA,'.-')
axis([0 t(end) -1 1])


%% Agregar una variación aleatoria
%R=random('Normal',0,0.2,1,length(t)); solo funciona con Statistics and Machine Learning Toolbox 
%Generacion de numeros aleatorios
a = 1;%desviacion estandar
b = 0;%media
R = a.*randn(1,length(t)) + b;
ETAr=ETA+R;
plot(t,ETAr,'.-')
%axis([0 t(end) -0.7 0.7])

%% Programar la Función de autocovarianza y de autocorrelaciòn 
y=X;
N=length(y);
ymean=mean(y);
k=0:fm*1022.5;%frecuencia de muestreo*desfase
%Calculo la funcion de autocovarianza             
for i=1:length(k) 
    for j=1:N-k(i)
        A(j)=(y(j)-ymean);
        B(j)=(y(j+k(i))-ymean);
    end
      Cyy(i)=(1/(N-k(i))).*sum(A.*B);
      clear A B
%         plot(t,y,t+k(i),y)
%         axis([t(1) t(150) -3 3])
%         pause
end
rho=Cyy/var(y); %Covarianza normalizada..
%a veces referida como función de autocorrelación...
per=k/fm; %periodicidades
figure
plot(per,rho,'.-r')






