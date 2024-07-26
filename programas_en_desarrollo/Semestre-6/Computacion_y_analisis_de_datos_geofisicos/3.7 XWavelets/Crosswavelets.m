a1=1; T1=10;e1=0;
a2=1; T2=5;e2=0;
fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=1024;
t=0:1/fm:endt-(1/fm);
X1=a1.*cos((2*pi/T1).*t+e1)+a2.*cos((2*pi/T2).*t+e2);
%Segunda señal
a1=0.15; T1=10;e1=0;
a2=0.1; T2=100;e2=0;
a3=0; T3=200;e3=0;
X2=a1.*cos((2*pi/T1).*t)+a2.*cos((2*pi/T2).*t+e2)+a3.*cos((2*pi/T3).*t+e3);
% %Tercer señal
% a1=0.2; T1=10;e1=0;
% a2=0.1;T2=50.5; e2=0;
% a3=0.1; T3=100;e3=0;
% X3=a1.*cos((2*pi/T1).*t)+a2.*cos((2*pi/T2).*t+e2)+a3.*cos((2*pi/T3).*t+e3);

%Generacion de numeros aleatorios
 a = 0.2;%desviacion estandar
 b = 0;%media
 R = a.*randn(1,length(t)) + b;
 
 X1=X1+R;
 X2=X2+R;
 clear a1 a2 a3 e1 e2 e3 endt T1 T2 T3 R a b
 
figure
 plot(X1)
 hold on
 plot(X2,'r')

%Calculamos el Wavelet cruzado
figure
xwtIMT(X1,X2,128,'ArrowDensity',[30 30]);%Modifica rutina en linea 170 para cambiar fm
figure
wtcIMT(X1,X2,128,'ArrowDensity',[30 30])

% [Wxy,period,scale,coi,sig95]=xwtIMT(X1,X2,64);
% magnitud=sqrt(real(Wxy).^2+imag(Wxy).^2);
% period_ajustado=period./fm;
% pcolor(t,log10(period_ajustado), magnitud); shading flat; colorbar
% ax=gca;
% ax.YScale = 'log';
% hold on
% plot(t,log10(coi),'w')


