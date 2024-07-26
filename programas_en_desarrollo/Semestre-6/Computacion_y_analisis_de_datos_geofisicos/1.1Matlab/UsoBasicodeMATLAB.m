%% Operaciones aritmèticas
20+30  % Orden de evaluación


a=20;b=30
c=a+b;

%triginométricas
lat=90*(pi/180);
sin(lat);

A=10; B=20;C=30;D=40;

T=A+3*B-2*sin(C*pi/180)-sqrt(D)
T2=A+3*B-2*sin(C*(pi/180))-sqrt(D)
T3=A+3*B-2*sin((C*(pi/180))-sqrt(D))
T4=A+3*(B-2)*sin(C*pi/180)-sqrt(D)

 %% Tipos de datos y formatos de datos en MATLAB

%% Formatos numéricos (single 32 bits y double 64 bits)
%Vectores m o n = 1
v1=[10 20 30]; v2=[10,20,30];%vectores renglón
v3=[10;20;30]; %vector columna
x1=0:0.01:1000;%secuencia de valores
x2=0:1e-2:1e3;%en notación científica

%Definir una matriz llena de un valor unico
B1=zeros(100);B2=zeros(100,200);
C1=ones(100);C2=ones(100,200);
D1=repmat(3,100);D2=repmat(3,100,200);

%Definir matrices aleatorias y mágicas
E1=rand(100);E2=rand(100,200);
F1=magic(100);
F2=sum(diag(F1));

%O con valores predeterminados
A0=[1,2,3; 4,5,6; 7,8,9;10,11,12]
A1=[1 2 3; 4 5 6; 7 8 9;10 11 12]
%comas y espacios separan valores en un renglon, punto y coma separa columnas
%para conocer las dimenciones de una matriz se usa:
size(A0)%para conocer renglones y matrices
%o podemos utilizar 
length(A0)
%para conocer el numero de elementos mas largo

%Multiplicaciòn de matrices renglón por columna y sumatoria de elementos
%se necesita A(mxp) B(pxn) y da como resultado C(mxn)
%C(i,j)=Sum(A(i,k)B(k,j);
A=[1,2,3; 4,5,6; 7,8,9]
v=[10 20 30];
D1=A*v';

%Multiplicación elemento por elemento: vector por matriz o matrices
%cuadradas de los mismos elementos
D2=A.*v';
v2=[10,20,30; 40,50,60];
D3=A.*v2;

A2=[1,2,3; 4,5,6; 7,8,9;10,11,12]
v3=[10,20,30; 40,50,60; 1, 2, 3; 4,5,6 ];
D4=A2.*v;

%No funciona si los elementos son dos matrices de dimensiones distintas
D5=A2.*v3;
D6=A2'.*v3;
%Como accesar datos en una matriz - operador : y funciones find, isnan
A2(:,1); A0(1,:);
A0(:)'
%definir una secuencia de valores y encontrarla en la matriz
s=1:3:12;
A2(s)
%O encontrar datos usando la función find
s1=find(A0>5)
s2=find(A1==1 | A1==10)
s3=find(A1>=1 & A1<=10)
[a,b]=find(A1>1 & A1<10)

s4=find(A0==s);%s es un vector, entonces debe hacerse en un ciclo (for o while)

for i=1:length(s)
 s4(i)=find(A0==s(i));
end
%Una vez encontrados los valores que se buscaban, podemos extraerlos de la
%matriz a un vector, o suplantarlos por otros valores:

v4=A0(s4);
A2=A0; A2(s4)=NaN
A3=isnan(A2)
s5=find(A3==1)
clear all

%Transformación de matrices
    A=magic(1000);
    B=flipud(A);
    C=fliplr(A);
    D=rot90(A);
    E=A';
    F=A(:);
    
  %Como visualizar datos  
    figure
    subplot(2,3,1)
    imagesc(A); caxis([0 100]); colormap jet; colorbar
    title('matriz A')
    ylabel('valor en y')
    subplot(2,3,2)
    imagesc(B); caxis([0 100]); colormap jet; colorbar
    title('flipud(A)')
    subplot(2,3,3)
    imagesc(C); caxis([0 100]); colormap jet; colorbar
    title('fliplr(A)')
    subplot(2,3,4)
    imagesc(D); caxis([0 100]); colormap jet; colorbar
    title('rot90(A)')
    subplot(2,3,5)
    imagesc(E); caxis([0 100]); colormap jet; colorbar
    title('A transpuesta')
    xlabel('valor en x')
    subplot(2,3,6)
    imagesc(F); caxis([0 100]); colormap jet; colorbar
    title('A(:)')
    xlabel('valor en x')
    
    A=magic(5);
    figure
    imagesc(A); colormap jet; colorbar; %caxis([0 1000000])
    title('imagesc')
    
    figure
    pcolor(A); caxis([0 1000000]); colormap jet; colorbar
    title('pcolor')
    shading flat
    shading interp
    
    
    
    
    %generar una figura 2D (scatter plot)
    X=0:0.01:30; b=1;
    Y=0.45*X+b;
    Y2=3.*sin(2*pi/3*X);
    Y3=Y2.*exp(0.5*X);
    
    figure
    plot(X,Y,':')
    hold on
    plot(X,Y2+Y)
   
    figure
    plot(X,Y,':',X,Y3)
    
    figure
    yyaxis left
    plot(X,Y)
    yyaxis right
    plot(X,Y2+Y)
    
    figure
    yyaxis left
    plot(X,Y)
    ylabel('lineal')
    yyaxis right
    plot(X,Y3)
    ylabel('exponencial')
    
    Am=mean(A); Av=var(A); As=std(A);Ama=max(A);Amin=min(A);
    Asq=sqrt(A);
    
% Funciones propias 
 function E=massequiv2(m)
%massequiv2 - Find energy from mass based on Einstein (1905)
%
% Syntax: energy = massequiv2(mass)
%
% Inputs:
% m - mass [kg]
%
% Outputs:
% E - equivalent energy [Joules or kg m^2 s^-2]
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% Author: Dave Heslop
% Department of Geosciences, University of Bremen
% email address: dheslop@uni-bremen.de
% Last revision: 6-Dec-2008
%------------- BEGIN CODE --------------
    c = 299792458; %speed of light [m s^-1]
    E = m.*c.^2; %calculate the energy in Joules [kg m^2 s^-2]
%------------- END CODE --------------
    
%% Characters y strings
%...Un "arreglo de caracteres" es una secuencia de letras, 
%justo como un arreglo numerico es una secuencia de numeros
N1=('Figura');%character - comillas simples
N2=['promedio de S'];

%Un string puede contener arreglos (matrices) de caracteres o texto simple 
N3=["promedio de S"];%string - comillas dobles
str = ["Mercury","Gemini","Apollo";"Skylab","Skylab B","ISS"];
Planeta=str(1,1)
str(2,3)
str(1,3)

%usar muchos char para generar un nombre mas complejo
nam=['Figura 10.2: promedio de S ']
S=10+(0:0.1:1);
s=num2str(S(3));
nam2=[N1,' ',s,':',N2];
nam3=num2str(zeros(length(S),1));
for i=1:length(S)
    s=num2str(S(i));
    nam2=[N1,' ',s,':',N2];
end
%ConvertCharsToStrings

%uso del comando eval
A1=("result=mean(S)");%string
A2=['mean(S)'];%Character
eval(A2)


%% Definicion de una tabla
T = table([10;20],{'M';'F'},'VariableNames',{'Age','Gender'},'RowNames',{'P1','P2'});
T2 = table(X',Y','VariableNames',{'X','Y'});
%Como accesar datos de la Tabla
b=mean(T2.X);

%% Definición de una estructura
field1 = 'X';  value1 = X;
field2 = 'Y';  value2 = Y;
field3 = 'Y2';  value3 = Y2;
field4 = 'T';  value4 = T;
field5 = 'Titulo';  value5 = {'Figura 10.2: promedio de S '};

s = struct(field1,value1,field2,value2,field3,value3,field4,value4,field5,value5);
clear field1 field2 field3 field4 field5 value1 value2 value3 value4 value5 b
mean(s.X)


%% Programación
%% Uso de ciclos
    
%ciclo for donde se conoce de antemano el numero de veces
%que se repite
X2=rand(10,1)*10;
for i=1:length(X2)
 x=X2(i)
 i
%  pause
% end
    if floor(x)==5; 
        A=("numero correcto")
        pause
    elseif x<5;
        B=("muy bajo")
        pause
    else
        C=("muy alto")
        pause
    end
end



%ciclo while donde no se conoce de antemano el numero
%de veces que se repite necesita un contador y un condicional
x=1;%este es valor inicial del contador
while x<6 %este es el condicional
     if x==5; 
        A=("right number")
        x
        pause
     else x<5;
        B=("too low")
        x
        pause
    end
    x=x+1;%este es el contador
end

X2=rand(1000,1)*10;
i=1;
while i>0 
 x=floor(X2(i));
 %  pause
% end
    if x==5; 
        A=("numero correcto")
        i
        pause
        i=-1;
    else
        display("no es")
        i=i+1;
    end
end

x=floor(X2);s=find(x==5);





