function matriz = struct2mat(structure)
    matriz = cell2mat(struct2cell(structure));
end