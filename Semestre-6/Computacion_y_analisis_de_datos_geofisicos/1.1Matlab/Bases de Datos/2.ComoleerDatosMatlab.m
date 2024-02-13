% 1.Copy and Paste
%A=ones(5,3);
% 2. load A.txt
% 3. A=dlmread('A.txt'); dlmwrite('A2.txt',A);
% 4. Leer/escribir de un archivo excel
data=xlsread('Alturas.xlsx','Hoja03','A1:J10');
%readmatrix("Alturas.xlsx",'Sheet','Hoja03','Range',['A1:J10']);
%writematrix(A,'Alturas.xlsx','Sheet','Hoja03','Range',['A1:J10']);
xlswrite('A2',A);
xlswrite('Alturas2.xlsx',A,'Hoja03','A1:J10');

%Archivo CTDdiver
fid1 = fopen('lancha2_221016211519_X1548.CSV', 'r');%r para leer read, para escribir w
%es un identificador; el numero negativo quiere decir que no lo pudo abrir.
   for j=1:64
   s = fgetl(fid1)
   end
   
   for j=1:18458
       s = fgetl(fid1);
       time(j)=datenum(s(1:19));
       p(j)=eval(s(21:27)); %cm
       t(j)=eval(s(29:34)); %C
       cond(j)=eval(s(36:end)); %mS/cm
   end
    
   fclose(fid1);
   clear ans fid1 j s 
   
   subplot(3,1,1)
   plot(time,p,'.')
   title('CTD Chelem')
   ylabel('Presion (mbar)')
   datetick
   subplot(3,1,2)
   plot(time,t,'.')
   ylabel('Temperatura(^o C)')
   datetick
   subplot(3,1,3)
   plot(time,cond,'.')
   ylabel('Conductividad(mS/cm)')
   datetick

  