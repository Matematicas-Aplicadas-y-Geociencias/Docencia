load NM_mensual.dat
plot(NM_mensual(:,2:end))
data=NM_mensual(:,2:end);

data=hilbert(data);
C=cov(data);%los datos deben estar acomodados con las columnas como cada serie de tiempo
[E,L]=eig(C);%eigenvectores y eigenvalores
%columnas son eigenvectores (modos), renglones son las estaciones espaciales.
var=diag(L)/trace(L);%los valores de varianza estan acomodados al reves

%Amplitud modal=componentes principales=Modos normales= la variación temporal
%Multiplicación tensorial
A=data*E;

%Para los Eigenvectores calcula amplitud y fase
AmpE=abs(E);
FaseE=angle(E);

%Para las Amplitud modal calcula(variacion temporal de...) amplitud y fase
AmpA=abs(A);
FaseA=angle(A);

figure
subplot(2,1,1)
plot(AmpE(:,8:9))
legend(num2str(var(8:9)))
xlabel('Estaciones mareograficas 1(sur) a 9 (norte)')
ylabel('Amplitud')
subplot(2,1,2)
plot(FaseE(:,8:9))
legend(num2str(var(8:9)))
xlabel('Estaciones mareograficas 1(sur) a 9 (norte)')
ylabel('Fase')

figure
subplot(2,1,1)
plot(NM_mensual(:,1),AmpA(:,8:9))
datetick
xlabel('tiempo')
ylabel('Amplitud')
subplot(2,1,2)
plot(NM_mensual(:,1),FaseA(:,8:9))
datetick
xlabel('tiempo')
ylabel('Fase')




