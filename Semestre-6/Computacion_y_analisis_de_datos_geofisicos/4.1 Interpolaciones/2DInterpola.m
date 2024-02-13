plot3(Perfiles(:,1),Perfiles(:,2),Perfiles(:,3),'.')

X=Perfiles(:,1)-min(Perfiles(:,1));
Y=Perfiles(:,2)-min(Perfiles(:,2));
Z=Perfiles(:,3);
%cortar zona sin datos Y<170
s1=find(Y>170)
plot(X(s1),Y(s1),'.')
X=X(s1);
Y=Y(s1);
Z=Z(s1);

plot3(X,Y,Z,'.')

dx=0.5; dy=0.5;%determine grid resolution
XI=min(X):dx:max(X);YI=min(Y):dy:max(Y);%X and Y vectors
[X2, Y2]= meshgrid(XI,YI); % create grid of x and y coordinates based on evenly spaced dataset
Z2 = griddata(X,Y,Z,X2,Y2,'cubic'); %'linear','cubic','nearest','natural', and 'v4' 
figure
pcolor(X2,Y2,Z2b);shading flat; colormap jet; colorbar; caxis([-9 3])
hold on
plot(X,Y,'.w')
surf(X2,Y2,Z2);;shading flat; colormap jet; colorbar;

%smooth the surface
Z2sm = smooth(Z2,5); 

%Other interpolation methods
% s2=1:1055;
% Z2b =interp2(X(s2),Y(s2),Z(s2),X2,Y2,'cubic'); %'linear','cubic','makima','spline' 


Z2b = barnes(X,Y,Z,X2,Y2,50,50,2);




