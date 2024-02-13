%como hacer video de imágenes jpg
%Aqui el nombre del video y su formato
vwObj = VideoWriter('BChinchorro', 'MPEG-4');
vwObj.FrameRate = 10;
open(vwObj);
catalogo=dir('*.jpg');

for i=1:length(catalogo)
   name=catalogo(i).name;
   I=imread (name);%Leer imagen
   h=imshow(I);%mostrarla
   %rect=[133 90 390 280]; %[left bottom width height] in pixels
   frame = getframe(gcf);%getframe(gcf,rect); en esta opcion solo obtienes una seccion del video
   writeVideo(vwObj, frame);
end
close(vwObj);
