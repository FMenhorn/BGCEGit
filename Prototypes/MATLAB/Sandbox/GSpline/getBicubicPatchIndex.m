

function bezierPoints = getBicubicPatchIndex(ind, As, Bs, Cs)
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
h_one_gen_rev = @(i,m_number, a_coef) ((1-2*a_coef)*Bs(:,1,i) + (1-2*a_coef)*Bs(:,2,mod_index(i-1,m_number)) + ...
    (5+2*a_coef)*Cs(:,i) + (5+2*a_coef)*Cs(:,mod_index(i-1,m_number)))/12;
h_one = @(i) h_one_gen(i,m,a);
%h_one_rev = @(i) h_one_gen_rev(i,m,a);
h_one_rev = @(i) h_one(mod_index(i-1,m));

% h_two_gen_part = @(i,l,m_number, a_coef, c_coef) Cs(:,l) + (2/3)*(a_coef/c_coef)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
%     (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l+1,m_number)));
h_two_gen_part = @(i,l,m_number, a_coef, c_coef,alpha) Cs(:,l) + (alpha)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
    (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l+1,m_number)));
h_two_gen_rev_part = @(i,l,m_number, a_coef, c_coef) Cs(:,l) + (2/3*a_coef/c_coef)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
    (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l-1,m_number)));
h_two_gen = @(i,m_number, a_coef, c_coef,alpha) h_two_gen_part(i,1:m_number,m_number,a_coef,c_coef,alpha)*ones(m_number,1)/m_number;
h_two_gen_rev = @(i,m_number, a_coef, c_coef) h_two_gen_rev_part(i,1:m_number,m_number,a_coef,c_coef)*ones(m_number,1)/m_number;
h_two = @(i) h_two_gen(i,m,a,c,2*a/(3*c));
%h_two_rev = @(i) h_two_gen_rev(i,m,a,c);
h_two_rev = @(i) h_two(mod_index(i-1,m));

h_three_gen = @(i,m_number,a_coef,c_coef) (1-2*c_coef/3)*h_two_gen(i,m_number,a_coef,c_coef) + ...
    h_one_gen(i,m_number,a_coef)*2*c_coef/3;
h_three = @(i) (1-2*c/3)*h_two(i) + h_one(i)*2*c/3;
%h_three_rev = @(i) (1-2*c/3)*h_two_rev(i) + h_one_rev(i)*2*c/3;
h_three_rev = @(i) h_three(mod_index(i-1,m));
% h_three = @(i) (1-c)*h_two(i) + h_one(i)*2*c/3;
% h_three_rev = @(i) (1-c)*h_two_rev(i) + h_one_rev(i)*c;

leftNeighbourIndexB = mod_index(ind-1,m);
leftNeighbourIndexC = mod_index(ind-1,m);

bezierPoints(:,1,1) = (Bs(:,2,ind) + Bs (:,1,ind) + Cs(:,ind) + As(:,ind) )*0.25;

bezierPoints(:,2,1) = (5*Bs(:,2,ind) + Bs (:,1,ind) + 5*Cs(:,ind) + As(:,ind) )/12;
bezierPoints(:,1,2) = (Bs(:,2,ind) + 5*Bs (:,1,ind) + 5*Cs(:,ind) + As(:,ind) )/12;

bezierPoints(:,3,1) = (5*Bs(:,2,ind) + Bs (:,1,mod_index(ind+1,m)) + 5*Cs(:,ind) + Cs(:,mod_index(ind+1,m)) )/12;
bezierPoints(:,1,3) = (5*Bs(:,1,ind) + Bs (:,2,leftNeighbourIndexB) + 5*Cs(:,ind) + Cs(:,leftNeighbourIndexC) )/12;

bezierPoints(:,4,1) = (Bs(:,2,ind) + Bs (:,1,mod_index(ind+1,m)) + Cs(:,ind) + Cs(:,mod_index(ind+1,m)) )*0.25;
bezierPoints(:,1,4) = (Bs(:,1,ind) + Bs (:,2,leftNeighbourIndexB) + Cs(:,ind) + Cs(:,leftNeighbourIndexC) )*0.25;

bezierPoints(:,2,2) = (5*Bs(:,2,ind) + 5*Bs (:,1,ind) + (25+4*a) * Cs(:,ind) + (1-4*a) * As(:,ind) )/36;

bezierPoints(:,3,2) = ((5-10*a)*Bs(:,2,ind) + (1+2*a)*Bs (:,1,mod_index(ind+1,m))...
    + (25+6*a) * Cs(:,ind) + (5+2*a) * Cs(:,mod_index(ind+1,m)) )/36;
bezierPoints(:,2,3) = ((5-10*a)*Bs(:,1,ind) + (1+2*a)*Bs (:,2,leftNeighbourIndexB) + ...
    (25+6*a) * Cs(:,ind) + (5+2*a) * Cs(:,leftNeighbourIndexC) )/36;

bezierPoints(:,4,4) = mean(Cs,2);

bezierPoints(:,4,2) = h_one(ind);
bezierPoints(:,2,4) = h_one_rev(ind);

bezierPoints(:,4,3) = h_two(ind);
bezierPoints(:,3,4) = h_two_rev(ind);
%if m is odd
if(mod(m,2) == 1 )
    for i = 1:m
        bezierPoints(:,3,3) = bezierPoints(:,3,3) ...
            - ((-1)^i) * h_three(mod_index(i+ind-1,m));
    end
else
    for i = 1:m
        bezierPoints(:,3,3) = bezierPoints(:,3,3) ...
            - ((-1)^i) * (m-i) * h_three(mod_index(i+ind-1,m));
    end 
    bezierPoints(:,3,3) = bezierPoints(:,3,3) * 2/m;
end

        



end