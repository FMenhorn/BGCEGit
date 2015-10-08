function bezierPoints = getBicubicPatch(A, Bs, Cs)
% nomenclature following that of paper of Eck, Hoppe (Automatic
% Reconstruction of B-Spline Surfaces of Arbitrary Topological Type), from
% which the formulae are also collected. Outputted is a 3x4x4 array of the
% bicubic patch bezier points, where the first dimension is the
% coordinates.

bezierPoints = zeros(3,4,4);

m = length(Cs);
c = cos(2*pi/m);
a = c/(1-c);

mod_index = @(i,modul) mod(i-1,modul) + 1;

h_one_gen = @(i,m_number, a_coef) ((1-2*a_coef)*Bs(:,2,i) + (1-2*a_coef)*Bs(:,1,mod_index(i+1,m_number)) + ...
    (5+2*a_coef)*Cs(:,i) + (5+2*a_coef)*Cs(:,mod_index(i+1,m_number)))/12;
h_one = @(i) h_one_gen(i,m,a);

h_two_gen_part = @(i,l,m_number, a_coef, c_coef) Cs(:,l) + (2/3*a_coef/c_coef)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
    (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l+1,m_number)));
h_two_gen = @(i,m_number, a_coef, c_coef) h_two_gen_part(i,1:m_number,m_number,a_coef,c_coef)*ones(m_number,1)/m_number;
h_two = @(i) h_two_gen(i,m,a,c);

h_three_gen = @(i,m_number,a_coef,c_coef) (1-2*c_coef/3)*h_two_gen(i,m_number,a_coef,c_coef) + ...
    h_one_gen(i,m_number,a_coef)*2*c_coef/3;
h_three = @(i) (1-2*c/3)*h_two(i) + h_one(i)*2*c/3;

leftNeighbourIndexB = m;
leftNeighbourIndexC = m;

bezierPoints(:,1,1) = (Bs(:,2,1) + Bs (:,1,1) + Cs(:,1) + A(:) )*0.25;

bezierPoints(:,2,1) = (5*Bs(:,2,1) + Bs (:,1,1) + 5*Cs(:,1) + A(:) )/12;
bezierPoints(:,1,2) = (Bs(:,2,1) + 5*Bs (:,1,1) + 5*Cs(:,1) + A(:) )/12;

bezierPoints(:,3,1) = (5*Bs(:,2,1) + Bs (:,1,2) + 5*Cs(:,1) + Cs(:,2) )/12;
bezierPoints(:,1,3) = (5*Bs(:,1,2) + Bs (:,2,leftNeighbourIndexB) + 5*Cs(:,1) + Cs(:,leftNeighbourIndexC) )/12;

bezierPoints(:,4,1) = (Bs(:,2,1) + Bs (:,1,2) + Cs(:,1) + Cs(:,2) )*0.25;
bezierPoints(:,1,4) = (Bs(:,1,1) + Bs (:,2,leftNeighbourIndexB) + Cs(:,1) + Cs(:,leftNeighbourIndexC) )*0.25;

bezierPoints(:,2,2) = (5*Bs(:,2,1) + 5*Bs (:,1,1) + (25+4*a) * Cs(:,1) + (1-4*a) * A(:) )/36;

bezierPoints(:,3,2) = ((5-10*a)*Bs(:,2,1) + (1+2*a)*Bs (:,1,2) + (25+6*a) * Cs(:,1) + (5+2*a) * Cs(:,2) )/36;
bezierPoints(:,2,3) = ((5-10*a)*Bs(:,1,1) + (1+2*a)*Bs (:,2,leftNeighbourIndexB) + ...
    (25+6*a) * Cs(:,1) + (5+2*a) * Cs(:,leftNeighbourIndexC) )/36;

bezierPoints(:,4,2) = h_one(1);
bezierPoints(:,2,4) = h_one(m);

bezierPoints(:,4,3) = h_two(1);
bezierPoints(:,3,4) = h_two(m);

bezierPoints(:,4,4) = mean(Cs,2);

%if m is odd
if(mod(m,2) == 1 )
    for i = 1:m
        bezierPoints(:,3,3) = bezierPoints(:,3,3) ...
            - ((-1)^i) * h_three(i);
    end
else
    for i = 1:m
        bezierPoints(:,3,3) = bezierPoints(:,3,3) ...
            - ((-1)^i) * (m-i) * h_three(i);
    end 
    bezierPoints(:,3,3) = bezierPoints(:,3,3) * 2/m;
end

        



end