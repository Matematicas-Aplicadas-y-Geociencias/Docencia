%% Read the contents of the file
inputFileName = 'Track.txt'; % Reemplaza con el nombre de tu archivo
fileContent = fileread(inputFileName);

%% Replace "a. m." with "AM" and "p. m." with "PM"
fileContent = regexprep(fileContent, '[a]\. [m]\.', 'AM');
fileContent = regexprep(fileContent, '[p]\. [m]\.', 'PM');

%% Search for date, time, latitude and longitude strings using regular expressions
dateTimePattern = '(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP][M])';
coordinatePattern = 'N(\d+\.\d+) W(\d+\.\d+)';

dateTimeMatches = regexp(fileContent, dateTimePattern, 'tokens');
coordinateMatches = regexp(fileContent, coordinatePattern, 'tokens');

%% Write the results to a new file
outputFileName = 'clean_satellite_data.txt';
fid = fopen(outputFileName, 'w');

fprintf('Date, time, latitude and longitude strings found!\n');
for i = 1:length(dateTimeMatches)
    dateTimeTokens = dateTimeMatches{i};

    % Converts 12-hours clock to 24-hour clock
    dateTime24 = string(datetime(dateTimeTokens{1}, 'InputFormat', 'dd/MM/yyyy hh:mm:ss a', 'Format', 'dd/MM/yyyy HH:mm:ss'));

    latitude = coordinateMatches{i}{1};
    longitude = coordinateMatches{i}{2};

    fprintf(fid, '%s, %s, %s\n', dateTime24, latitude, longitude);
end

fclose(fid);