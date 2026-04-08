%% Script para descargar datos históricos de www.hycom.org
%{
    Title:          HYCOM-TSIS GOMe0.01
    Resolution:     1/100º (~1 km)
    Domain:         Extends from 98ºE to 77ºE in longitude
                    and from 18ºN to 32ºN in latitude
    Vertical 
    resolution:     41 hybrid layers
    Institution:    Center for Ocean-Atmospheric Prediction Studies (COAPS)
    Date/
    Data Range:     2024-09-01 to "Present" (1-6 month delay)
    HYCOM version:  2.3.01

    Experiment numbers:
    YYYY: year, DDD: day, HH: hour, NN: Netcdf type (i.e. 2d or 3z)
    HYCOM-TSIS GOMe0.01:
    028_archv.YYYY_DDD_HH_NN.nc: 2024_245_19 to *PRESENT*
%}
% Configuración inicial
clc; clear; close all;

%% Solicitar parámetros al usuario
% --------------------------------------------------------
% Crear cuadro de diálogo para entrada de datos
prompt = {
    'Fecha inicial (yyyy-DDD-HH):';
    'Fecha final (yyyy-DDD-HH):';
    'Intervalo temporal (horas):'
};
dlgtitle = 'Parámetros de entrada';
dims = [1 50];
definput = {
    '2024-245-19', '2024-246-01', '1'
};

% Obtener valores del usuario
answer = inputdlg(prompt, dlgtitle, dims, definput);

% Validar que se ingresaron todos los parámetros
if isempty(answer)
    error('Entrada cancelada por el usuario');
end

%% Procesar parámetros ingresados
% --------------------------------------------------------
% Procesar fechas
try
    startDate = datetime(answer{1}, 'InputFormat', 'uuuu-DDD-HH');
    endDate = datetime(answer{2}, 'InputFormat', 'uuuu-DDD-HH');
    
    % Validar intervalo temporal
    hourStep = str2double(answer{3}); %Datos por hora
    if isnan(hourStep) || hourStep <= 0
        error('Intervalo temporal inválido');
    end
catch ME
    error(['Error en formato de fecha: ' ME.message]);
end

%% Configurar directorio de resultados
% --------------------------------------------------------
resultDirectory = fullfile(pwd, 'Data');
if ~exist(resultDirectory, 'dir')
    mkdir(resultDirectory);
end

%% Configurar Timeout de la descarga
% --------------------------------------------------------
options = weboptions('Timeout', 300);

%% Mostrar resumen de parámetros
% --------------------------------------------------------
fprintf('\n=== Parámetros de descarga ===\n');
fprintf('\nRango temporal:\n');
fprintf(' Inicio: %s\n Fin: %s\n Intervalo: %d horas\n',...
    char(datetime(startDate, 'Format', 'dd-MMM-uuuu HH:mm')),...
    char(datetime(endDate, 'Format', 'dd-MMM-uuuu HH:mm')),...
    hourStep);
fprintf('\nDirectorio de salida: %s\n\n', resultDirectory);

%% Bucle principal de descargas
% --------------------------------------------------------
currentTime = startDate;
while currentTime <= endDate
    error_flag = true;
    
    while error_flag
        try
            %% Construir URL
            url = sprintf(['https://data.hycom.org/datasets/GOMe0.01/expt_02.8/data/archive/%04d/' ...
                '028_archv.%04d_%03d_%02d_2d.nc'],...
                year(currentTime),year(currentTime), day(currentTime, "dayofyear"), hour(currentTime));
            
            %% Configurar nombre de archivo
            fileName = ['028_archv.' char(datetime(currentTime, 'Format', 'uuuu_DDD_HH')) '_2d.nc'];
            outputFile = fullfile(resultDirectory, fileName);
            
            %% Descargar archivo
            websave(outputFile, url, options);
            fprintf('Descarga exitosa: %s\n', fileName);
            error_flag = false;
            
        catch ME
            fprintf(2, 'Error en descarga: %s\n', ME.message);
            fprintf('Reintentando en 8 segundos...\n');
            pause(8);
        end
    end
    
    %% Avanzar al siguiente intervalo
    currentTime = currentTime + hours(hourStep);
end

fprintf('\n=== Descarga completada ===\n');