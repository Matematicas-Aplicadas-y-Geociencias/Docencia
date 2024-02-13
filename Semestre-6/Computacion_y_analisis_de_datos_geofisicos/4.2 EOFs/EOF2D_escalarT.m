load SST_2009_2012
%datos cada 5 dias

for i =1:length(time)
    pcolor(lon,lat,ssh(:,:,i))
    shading flat
    colorbar
    title(datestr(time(i),'yyyy/mm/dd'))
    pause(.01)
end


%Reorganizar base de datos con reshape para
%poder tener "series de tiempo" en las columnas
data=reshape(tt,8464,292);
    %prueba de que el reshape funciona (obtener matriz espacial de regreso)
%     B=reshape(data,92,92,292);
%     pcolor(lon,lat,B(:,:,1))
%     shading flat
%     clear B
    %La mascara de tierra son NaNs, hay que quitarlos
    %para hacer los EOFs...en este caso se hacen ceros
s1=isnan(data);
s2=find(s1==1);%Mascara de NaNs
s3=find(s1==0);
data2=data;
data2(s2)=0;

%Matriz de temperatura promedio espacial
Tmean=mean(data2');
 %Verifica el comportamiento espacial del promedio
%     B=reshape(Tmean,92,92);
%     pcolor(lon,lat,B)
%     shading flat
%     colorbar
%     caxis([22.5 28])
%     clear B
%  
%Calcula matriz de anomalía térmica (quitar el comportamiento promedio  a
%los datos)

for i=1:292
  data3(:,i)=data2(:,i)-Tmean';
end

%Calcular matriz de covarianza 
C = data3*data3';%MxN X NxM=MxM
[E,L]=eig(C);%eigenvectores y eigenvalores
%En E las columnas son eigenvectores (modos), renglones son las estaciones espaciales.
var=diag(L)/trace(L);%los valores de varianza estan acomodados al reves
%Amplitud modal(AM)=componentes principales=Modos normales= la variación temporal
%Multiplicación tensorial
A=data3'*E;
%Segun el cuadro de Preisendorfer, para 9 series con 200 puntos, para el
%modo 1 (j=1) se necesita de menos un 15% para que sea válido...osea que
%solo los modos 1 y 2 (columnas 9 y 10) son las utiles. 

EM=reshape(E,92,92,8464);

figure
pcolor(lon,lat,EM(:,:,8464))%En 292
shading flat
colormap(jet)
colorbar
title(['EOF01  ', num2str(var(8464))])
% caxis([420 500])

figure
pcolor(lon,lat,EM(:,:,8462))%En 292
shading flat
colormap(jet)
colorbar
title(['EOF02  ', num2str(var(8463))])

%Grafico de serie de tiempo
figure
subplot(2,1,1)
plot(time,A(:,8464))
datetick
legend(num2str(var(8464)*100))
xlabel('tiempo')
ylabel('Variaciones térmicas')
subplot(2,1,2)
plot(time,A(:,8463))
datetick
legend(num2str(var(8463)*100))
xlabel('tiempo')
ylabel('Variaciones térmicas')


%Ejemplo para un tiempo en específico
FEOt=(EM(:,:,8464)*A(53,8464))+(EM(:,:,8463)*A(53,8463));
FEOt2=FEOt+reshape(Tmean,92,92);

figure
pcolor(lon,lat,FEOt)%En 292
shading flat
colormap(jet)
colorbar
title(['Sumatoria de EOF01 y EOF02 '])

