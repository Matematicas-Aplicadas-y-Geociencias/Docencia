%Ortogonalidad de funciones
a1=1; T1=10;e1=0;
a2=1; T2=5;e2=0;
fm=2;%Hz frecuencia de muestreo en ciclos por tiempo
endt=15;
t=0:1/fm:endt-(1/fm);
X1=a1.*sin(((2*pi)/T1).*t);
X2=a2.*sin(((2*pi)/T2).*t);

sum(X1.*X2)

load NM_mensual.dat %datos de nivel del mar promedio mensual en mm
for i=2:10
 plot(NM_mensual(:,1),NM_mensual(:,i))
 hold on
 axis([NM_mensual(1,1) NM_mensual(end,1) -400 400])
 title(num2str(i))
 hold off
 pause
end
 
pcolor(1:9,NM_mensual(:,1),NM_mensual(:,2:end)); shading flat; colorbar

Psi=NM_mensual(13:end,2:end);%13 para que combine bien con el tamaño de MEI
Psip=Psi-mean(Psi);%Datos sin promedio en cada punto del espacio

C=cov(Psip);%los datos deben estar acomodados con las columnas como cada serie de tiempo
[Phi,L]=eig(C);%eigenvectores y eigenvalores para calcular varianza explicada
%columnas son eigenvectores (modos), renglones son las estaciones espaciales.
var=diag(L)/trace(L);%cada eigenvalor entre su suma...los valores de varianza estan acomodados al reves

%Amplitud modal=componentes principales=Modos normales= la variación temporal
%Multiplicación matricial
a=Psip*Phi;


figure
subplot(3,1,1)
plot(Phi(:,8:9))
legend(num2str(var(8:9)))
xlabel('Estaciones mareograficas 1(sur) a 9 (norte)')
ylabel('Elevaciones sin unidades')
subplot(3,1,2)
plot(NM_mensual(13:end,1),a(:,8:9))
axis([NM_mensual(13,1) NM_mensual(end,1) -500 1000])
subplot(3,1,3)
plot(NM_mensual(13:end,1),a(:,9).*Phi(9,9))

%% los datos del MEI se cortan para tener las mismas fechas que los datos de
%nivel del mar
MEI=dlmread('MEI.txt');
MEIb=MEI(1:22,2:13)';
MEIc=MEIb(:);

tMEI=[MEI(1:22,1)+(0.5:11.5)/12]';
tMEIc=tMEI(:);

subplot(3,1,3)
plot(tMEIc,MEIc)
axis([tMEIc(1) tMEIc(end) -2 3])
grid

%% Espectro cruzado entre la señal del Niño y el EOF
X1=detrend(MEIc,0);
X2=detrend(a(:,9),0);
s=2^9; %preferencia un multiplo de 2^n
X1(end+1:s)=0;
X2(end+1:s)=0;

N=length(X1);
fm=12;
m=128;
n=m/2;
window=hanning(m);
[XSp01,F]=cpsd(X1,X2,hanning(m),n,m,fm);
[Coh01,F]=mscohere(X1,X2,hanning(m),n,m,fm);

%Calculo de la fase entre las series de tiempo
ph=angle(XSp01);
%ph=unwrap(ph); %avoids sudden jumps in the phase
%Convertir a grados de radianes
Ph01=ph.*(180./pi);
%limites de confianza para la coherencia
cl=0.95; 
NOI=N./m; %No. of non-overlapping intervals
dof=3.82.*NOI-3.24; %degrees of freedom if Hanning window is used
conf=1-cl; %At 95% confidence limit
Clim=1-conf.^(1/((0.5*dof)-1));
li=[F(2) F(end-1)]; %Confidence limit vectors
w=[Clim Clim];

figure
subplot(3,1,1)
semilogx(F,real(XSp01),'k')
hold on
semilogx(F,imag(XSp01),'r')
subplot(3,1,2)
semilogx(F,Coh01)
hold on
semilogx(li,w,'r')
subplot(3,1,3)
semilogx(F,Ph01,'or')

%% Calculamos el Wavelet cruzado
figure
xwtIMT(X1,X2,12,'ArrowDensity',[30 30]);
xticks(tMEIc)
figure
wtcIMT(X1,X2,12,'ArrowDensity',[30 30])
