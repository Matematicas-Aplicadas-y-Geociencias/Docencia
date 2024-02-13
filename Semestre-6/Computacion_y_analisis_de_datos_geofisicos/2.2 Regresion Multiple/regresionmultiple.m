% Cargar datos para regresion 2D

x1=airqual2023.CO;
x2=airqual2023.Temperatura;
y=airqual2023.Benceno;%Probar Iridio,Titanio, Tungsteno

plot3(x1,x2,y,'.')
xlabel('CO')
ylabel('Temp')
zlabel('Benceno')
grid


x1mean = mean(x1);
x2mean = mean(x2);
ymean = mean(y);

% despues calculamos las correlaciones entre las variables
rX1X2num = sum((x1 - x1mean).*(x2 - x2mean));%Covarianza entre X1 y X2
rX1X2den = sqrt(sum((x1 - x1mean).^2)*sum((x2 - x2mean).^2));%StdDevX1 y X2
rX1X2= rX1X2num/rX1X2den;

% El método directo. 
% Se puede hacer facilmente en matlab con la función corr()
r12 = corr(x1,x2);%Correlacion entre X1 y X2
r1y = corr(x1,y);%Correlacion entre X1 y Y
r2y = corr(x2,y);%Correlacion entre Y y X2

% luego calculamos las desviaciones estándar de las variables
% se puede usar la función std()
%Sx1b = sqrt(sum((x1-x1mean).^2)./length(x1));

%Directamente con la funciòn std
Sx1=std(x1);
Sx2=std(x2);
Sy=std(y);

% calculamos las m' normalizadas usando correlaciones
mprimx1= (r1y - r2y*r12)/(1 - (r12)^2); 
mprimx2= (r2y - r1y*r12)/(1 - (r12)^2); 

%transformar ecuación estandarizada a común
mx1= mprimx1*(Sy/Sx1);
mx2= mprimx2*(Sy/Sx2);

%Calcular ordenada al origen
bord = ymean - (mx1*x1mean)-(mx2*x2mean);

%Aqui se programa la ecuación y se grafica en 3D
x1b=0:0.2:12;
x2b=-5:0.25:45;
[X1,X2]=meshgrid(x1b,x2b);
Y=(mx1*X1+mx2*X2)+bord;

figure
surf(X1,X2,Y); shading interp
hold on
plot3(x1,x2,y,'.k')
colorbar
xlabel('CO')
ylabel('Temp')
zlabel('Benceno')
grid

%Para calcular R^2
R2 = r1y*mprimx1 + r2y*mprimx2;



%cómo se hace más rápido
% n = length(x1);
% a = [ones(n,1) x1 x2];
% c = pinv(a)*y;
% el primer valor de c es la ordenada al origen, el segundo mx1, el tercero
% es mx2. Queda bastante similar a lo obtenido.




