%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
eta=detrend(NivelMar);
%x1=detrend(VN);
x2=detrend(VE);
%y1=detrend(WN);
y2=detrend(WE);
%T1=detrend(TempOcean);
fm=48;%debe de cambiarse a este valor en las rutinas cwt_IMT y xwt_IMT
t=tOcean;
 
%Calculamos el Wavelet cruzado modificar para tiempo en lineas 174 y 207
figure
xwtIMT(eta,x2,128,'ArrowDensity',[35 35]);%Modifica rutina en linea 170 para cambiar fm
figure
wtcIMT(eta,x2,128,'ArrowDensity',[35 35])

figure
xwtIMT(y2,x2,128,'ArrowDensity',[35 35]);%Modifica rutina en linea 170 para cambiar fm
figure
wtcIMT(y2,x2,128,'ArrowDensity',[35 35])




