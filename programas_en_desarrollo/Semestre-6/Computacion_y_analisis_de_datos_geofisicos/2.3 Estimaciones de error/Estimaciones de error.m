%Estimaciones de error modelo-mediciones
%           tm=tiempo del modelo
%           Um= Componente Este-Oeste modelada
%           Vm= Componente Norte-Sur modelada
%           to=tiempo de las observaciones
%           Um= Componente Este-Oeste observada
%           Vm= Componente Norte-Sur observada
% Puedes calcularlo tambien  con las elevaciones (marea). Y para las
% magnitudes de la velocidad
load Obs_vs_modeloCozumel.mat
Vmod=sqrt((Um.^2)+(Vm.^2));%mod de modelo
Vobs=sqrt((Uo.^2)+(Vo.^2));%obs de observaciones
%1. Asegurar que los vectores a comparar abarcan el mismo tiempo y tienen
%la misma frecuencia de muestreo. 
plot(tm,Vmod); hold on; plot(to,Vobs,'r')
legend('Modelo','Observaciones')
datetick('x','dd/mmm/yy')
%aqui se interpola con el tiempo de las observaciones para asegurar mismo tamaño de vectores
VmodI=interp1(tm,Vmod,to);


%% Comparacion por parametros de dispersion y error
%RMSE - error cuadrático medio...en unidades de la variable, análogo a la
%desviación estándar
x=Vobs;y=VmodI;
N=length(x);
RMSE=sqrt((sum((x-y).^2))./N);

%Coeficiente de determinación (R^2)
%rcuadrada
xmean = mean(x);
ymean = mean(y);
SSX=sum((x-xmean).^2);%similar a la varianza en x
SSY=sum((y-ymean).^2);%similar a la varianza en y
SSXY=sum((x-xmean).*(y-ymean));%similar a la co-varianza
m = SSXY/SSX;
R2 = (m .* SSXY)/SSY;

%Coeficiente de Nash-Suttclife...entre mas cercano a 1, mejor
NS=1-(sum((x-y).^2)/SSX);

%% Histograma
%lo primero es definir un rango en x para el histograma
edges=0:0.05:2.5;
[n,x]=histcounts(x,edges);
[n2,x]=histcounts(y,edges);
%aqui se convirtio numero de observaciones en porcentajes 
npercent=(n/N)*100;
n2percent=(n2/N)*100;
%esta parte grafica el histograma de velocidades promediadas en la vertical
%y sobrepone los pocentajes cumulativos
bar(x(2:end),npercent,'g');
ylabel('Porcentajes')
xlabel('Velocidad (m/s2)')
hold on
bar(x(2:end),n2percent,'r');
legend('Observaciones','Modelo');
alpha(0.5)%agregar transparencia a figura

