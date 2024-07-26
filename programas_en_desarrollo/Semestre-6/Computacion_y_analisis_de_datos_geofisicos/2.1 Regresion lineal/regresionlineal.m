
% wine consumption,	liquor consumption, cirrhosis death rate
% Empezar con wine consumption vs cirrhosis death rate

%x= cirrhosisd.wine;
x=cirrhosisd.liq;
y= cirrhosisd.cirrosis;

plot(x,y,'o')
xlabel('Consumo de vino')
ylabel('Muertes por cirrosis')

%ajustar linea por mínimos cuadrados
xmean = mean(x);
ymean = mean(y);

SSX=sum((x-xmean).^2);%similar a la varianza en x
SSY=sum((y-ymean).^2);%similar a la varianza en y
SSXY=sum((x-xmean).*(y-ymean));%similar a la co-varianza

%Calculo de la pendiente y la ordenada al origen
m = SSXY/SSX;
b = ymean -(m*xmean);
x2=0:150;
y2=m.*x2+b;

plot(x,y,'o')
xlabel('Consumo de vino')
ylabel('Muertes por cirrosis')
hold on
plot(x2,y2,'r')

%Cálculo de R^2
 Rcuad = (m .* SSXY)/SSY;










