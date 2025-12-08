%% Script para descargar datos históricos de www.hycom.org
% Configuración inicial
clc; clear; close all;

%% Solicitar parámetros al usuario
% --------------------------------------------------------
% Crear cuadro de diálogo para entrada de datos
prompt = {
    'Longitud Este:'; 
    'Longitud Oeste:';
    'Latitud Sur:';
    'Latitud Norte:';
    'Fecha inicial (dd-MMM-yyyy HH:mm:ss):';
    'Fecha final (dd-MMM-yyyy HH:mm:ss):';
    'Intervalo temporal (horas):'
};
dlgtitle = 'Parámetros de entrada';
dims = [1 50];
definput = {
    '-79.49032833399365', '-98.6159222300094', '16.316667463236794', '30.736758099121694',...
    '04-APR-2022 18:00:00', '04-APR-2022 19:00:00', '1'
};

% Obtener valores del usuario
answer = inputdlg(prompt, dlgtitle, dims, definput);

% Validar que se ingresaron todos los parámetros
if isempty(answer)
    error('Entrada cancelada por el usuario');
end

%% Procesar parámetros ingresados
% --------------------------------------------------------
% Convertir coordenadas a números
try
    east = str2double(answer{1});
    west = str2double(answer{2});
    south = str2double(answer{3});
    north = str2double(answer{4});
    
    % Validar coordenadas numéricas
    if any(isnan([east, west, south, north]))
        error('Valores geográficos inválidos');
    end
    
    % Validar rangos geográficos
    if west > -98
        error('Longitud Oeste fuera de rango.');
    end
    if east > -77 
        error('Longitud Este fuera de rango.');
    end
    if south > 19
        error('Latitud Sur fuera de rango.');
    end
    if north > 31
        error('Latitud Norte fuera de rango.');
    end
catch
    error('Error en formato de coordenadas. Usar números decimales');
end

% Procesar fechas
try
    startDate = datetime(answer{5}, 'InputFormat', 'dd-MMM-yyyy HH:mm:ss', 'Locale', 'en_US');
    endDate = datetime(answer{6}, 'InputFormat', 'dd-MMM-yyyy HH:mm:ss', 'Locale', 'en_US');
    
    % Validar intervalo temporal
    timeStep = str2double(answer{7});
    if isnan(timeStep) || timeStep <= 0
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
fprintf('Región geográfica:\n');
fprintf(' Este: %.2f°E\n Oeste: %.2f°O\n Sur: %.2f°S\n Norte: %.2f°N\n', east, west, south, north);
fprintf('\nRango temporal:\n');
fprintf(' Inicio: %s\n Fin: %s\n Intervalo: %d horas\n',...
    char(datetime(startDate, 'Format', 'dd-MMM-yyyy HH:mm')),...
    char(datetime(endDate, 'Format', 'dd-MMM-yyyy HH:mm')),...
    timeStep);
fprintf('\nDirectorio de salida: %s\n\n', resultDirectory);

%% Bucle principal de descargas
% --------------------------------------------------------
currentTime = startDate;
while currentTime <= endDate
    error_flag = true;
    
    while error_flag
        try
            %% Construir URL
            url = sprintf(['https://ncss.hycom.org/thredds/ncss/GOMb0.01/reanalysis/%04d/' ...
                '3z?var=salinity&var=u&var=v&var=w_velocity&var=water_temp&'...
                'north=%.4f&west=%.4f&east=%.4f&south=%.4f&' ...
                'disableProjSubset=on&horizStride=1&' ...
                'time=%s&vertCoord=1&accept=netcdf4'],...
                year(currentTime),north, west, east, south,...
                urlencode(char(datetime(currentTime, 'Format', 'yyyy-MM-dd''T''HH:mm:ss''Z'''))));
            
            %% Configurar nombre de archivo
            fileName = [char(datetime(currentTime, 'Format', 'yyyyMMdd_HH')) '.nc'];
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
    currentTime = currentTime + hours(timeStep);
end

fprintf('\n=== Descarga completada ===\n');