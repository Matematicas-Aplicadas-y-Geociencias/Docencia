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