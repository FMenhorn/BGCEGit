%% createBicubicCoefMatrices

function [Acoefs, B1coefs, B2coefs, Ccoefs] = createBicubicCoefMatrices(num_of_quads)

% returns a matrix with the biquadractic point coefficients of its
% neighbour vertices for each control point (i,j) on the bicubic patch,
% in the form of four vectors of neighbouring vertex point coefs

% nomenclature following that of paper of Eck, Hoppe (Automatic
% Reconstruction of B-Spline Surfaces of Arbitrary Topological Type), from
% which the formulae are also collected. (except that indices of the
% control points are, following matlab custom, shifted one higher ;-)  )

Acoefs = zeros(num_of_quads,4,4);
B1coefs = zeros(num_of_quads,4,4);
B2coefs = zeros(num_of_quads,4,4);
Ccoefs = zeros(num_of_quads,4,4);

c = cos(2*pi/num_of_quads);
a = c/(1-c);

mod_index = @(i,modul) mod(i-1,modul) + 1;

% h_one_gen = @(i,m_number, a_coef) ((1-2*a_coef)*Bs(:,2,i) + (1-2*a_coef)*Bs(:,1,mod_index(i+1,m_number)) + ...
%     (5+2*a_coef)*Cs(:,i) + (5+2*a_coef)*Cs(:,mod_index(i+1,m_number)))/12;
% h_one_gen_rev = @(i,m_number, a_coef) ((1-2*a_coef)*Bs(:,1,i) + (1-2*a_coef)*Bs(:,2,mod_index(i-1,m_number)) + ...
%     (5+2*a_coef)*Cs(:,i) + (5+2*a_coef)*Cs(:,mod_index(i-1,m_number)))/12;
% h_one = @(i) h_one_gen(i,num_of_quads,a);
% %h_one_rev = @(i) h_one_gen_rev(i,m,a);
% h_one_rev = @(i) h_one(mod_index(i-1,num_of_quads));
% 
% % h_two_gen_part = @(i,l,m_number, a_coef, c_coef) Cs(:,l) + (2/3)*(a_coef/c_coef)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
% %     (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l+1,m_number)));
% h_two_gen_part = @(i,l,m_number, a_coef, c_coef,alpha) Cs(:,l) + (alpha)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
%     (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l+1,m_number)));
% h_two_gen_rev_part = @(i,l,m_number, a_coef, c_coef) Cs(:,l) + (2/3*a_coef/c_coef)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
%     (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l-1,m_number)));
% h_two_gen = @(i,m_number, a_coef, c_coef,alpha) h_two_gen_part(i,1:m_number,m_number,a_coef,c_coef,alpha)*ones(m_number,1)/m_number;
% h_two_gen_rev = @(i,m_number, a_coef, c_coef) h_two_gen_rev_part(i,1:m_number,m_number,a_coef,c_coef)*ones(m_number,1)/m_number;
% h_two = @(i) h_two_gen(i,num_of_quads,a,c,2*a/(3*c));
% %h_two_rev = @(i) h_two_gen_rev(i,m,a,c);
% h_two_rev = @(i) h_two(mod_index(i-1,num_of_quads));
% 
% h_three_gen = @(i,m_number,a_coef,c_coef) (1-2*c_coef/3)*h_two_gen(i,m_number,a_coef,c_coef) + ...
%     h_one_gen(i,m_number,a_coef)*2*c_coef/3;
% h_three = @(i) (1-2*c/3)*h_two(i) + h_one(i)*2*c/3;
% %h_three_rev = @(i) (1-2*c/3)*h_two_rev(i) + h_one_rev(i)*2*c/3;
% h_three_rev = @(i) h_three(mod_index(i-1,num_of_quads));
% % h_three = @(i) (1-c)*h_two(i) + h_one(i)*2*c/3;
% % h_three_rev = @(i) (1-c)*h_two_rev(i) + h_one_rev(i)*c;
% 
% leftNeighbourIndexB = mod_index(ind-1,num_of_quads);
% leftNeighbourIndexC = mod_index(ind-1,num_of_quads);

% i,j = 1,1
%bezierPoints(:,1,1) = (Bs(:,2,ind) + Bs (:,1,ind) + Cs(:,ind) + As(:,ind) )*0.25;
B1coefs(1,1,1) = 0.25;
B2coefs(1,1,1) = 0.25;
Ccoefs(1,1,1) = 0.25;
Acoefs(1,1,1) = 0.25;

% i,j = 1,2 or 2,1
% bezierPoints(:,2,1) = (5*Bs(:,2,ind) + Bs (:,1,ind) + 5*Cs(:,ind) + As(:,ind) )/12;
% bezierPoints(:,1,2) = (Bs(:,2,ind) + 5*Bs (:,1,ind) + 5*Cs(:,ind) + As(:,ind) )/12;
B1coefs(1,2,1) = 1/12;
B2coefs(1,2,1) = 5/12;
Ccoefs(1,2,1) = 5/12;
Acoefs(1,2,1) = 1/12;

%i,j = 3,1
% bezierPoints(:,3,1) = (5*Bs(:,2,ind) + Bs (:,1,mod_index(ind+1,num_of_quads)) + 5*Cs(:,ind) + Cs(:,mod_index(ind+1,num_of_quads)) )/12;
% bezierPoints(:,1,3) = (5*Bs(:,1,ind) + Bs (:,2,leftNeighbourIndexB) + 5*Cs(:,ind) + Cs(:,leftNeighbourIndexC) )/12;

B2coefs(1,3,1) = 5/12;
B1coefs(2,3,1) = 1/12;
Ccoefs(1,3,1) = 5/12;
Ccoefs(2,3,1) = 1/12;

%i,j = 4,1
% bezierPoints(:,4,1) = (Bs(:,2,ind) + Bs (:,1,mod_index(ind+1,num_of_quads)) + Cs(:,ind) + Cs(:,mod_index(ind+1,num_of_quads)) )*0.25;
% bezierPoints(:,1,4) = (Bs(:,1,ind) + Bs (:,2,leftNeighbourIndexB) + Cs(:,ind) + Cs(:,leftNeighbourIndexC) )*0.25;

B2coefs(1,4,1) = 0.25;
B1coefs(2,4,1) = 0.25;
Ccoefs(1,4,1) = 0.25;
Ccoefs(2,4,1) = 0.25;

%i,j = 2,2
% bezierPoints(:,2,2) = (5*Bs(:,2,ind) + 5*Bs (:,1,ind) + (25+4*a) * Cs(:,ind) + (1-4*a) * As(:,ind) )/36;

B2coefs(1,2,2) = 5/36;
B1coefs(1,2,2) = 5/36;
Ccoefs(1,2,2) = (25 + 4*a)/36;
Acoefs(1,2,2) = (1 - 4*a)/36;

%i,j = 3,2
% bezierPoints(:,3,2) = ((5-10*a)*Bs(:,2,ind) + (1+2*a)*Bs (:,1,mod_index(ind+1,num_of_quads))...
%     + (25+6*a) * Cs(:,ind) + (5+2*a) * Cs(:,mod_index(ind+1,num_of_quads)) )/36;
% bezierPoints(:,2,3) = ((5-10*a)*Bs(:,1,ind) + (1+2*a)*Bs (:,2,leftNeighbourIndexB) + ...
%     (25+6*a) * Cs(:,ind) + (5+2*a) * Cs(:,leftNeighbourIndexC) )/36;
B2coefs(1,3,2) = (5-10*a)/36;
B1coefs(2,3,2) = (1+2*a)/36;
Ccoefs(1,3,2) = (25+6*a)/36;
Ccoefs(2,3,2) = (5+2*a)/36;

%i,j = 4,4
% bezierPoints(:,4,4) = mean(Cs,2);
Ccoefs(:,4,4) = 1/num_of_quads;

%i,j = 4,2
% bezierPoints(:,4,2) = h_one(ind);
% bezierPoints(:,2,4) = h_one_rev(ind);
% h_one_gen = @(i,m_number, a_coef) ((1-2*a_coef)*Bs(:,2,i) + (1-2*a_coef)*Bs(:,1,mod_index(i+1,m_number)) + ...
%     (5+2*a_coef)*Cs(:,i) + (5+2*a_coef)*Cs(:,mod_index(i+1,m_number)))/12;
B2coefs(1,4,2) = (1-2*a)/12;
B1coefs(2,4,2) = (1-2*a)/12;
Ccoefs(1,4,2) = (5+2*a)/12;
Ccoefs(2,4,2) = (5+2*a)/12;

%i,j = 4,3
% bezierPoints(:,4,3) = h_two(ind);
% bezierPoints(:,3,4) = h_two_rev(ind);
% h_two_gen_part = @(i,l,m_number, a_coef, c_coef,alpha) Cs(:,l) + (alpha)*cos(2*pi*ones(3,1)*reshape(l,1,length(l))/m_number).*...
%     (Cs(:,mod_index(i+l,m_number)) + Cs(:,mod_index(i+l+1,m_number)));
% h_two_gen = @(i,m_number, a_coef, c_coef,alpha) h_two_gen_part(i,1:m_number,m_number,a_coef,c_coef,alpha)*ones(m_number,1)/m_number;
% h_two = @(i) h_two_gen(i,num_of_quads,a,c,2*a/(3*c));
Ccoefs(:,4,3) = Ccoefs(:,4,3) + 1/num_of_quads;
for l = 1:num_of_quads
    Ccoefs(l,4,3) = Ccoefs(l,4,3) + (2*a/(3*c*num_of_quads)) * (cos(2*pi*(l-2)/num_of_quads) + cos(2*pi*mod_index(l-1,num_of_quads)/num_of_quads) );
end


% create all the symmetric coefficients from symmetry

reversedIndices = num_of_quads:1;
shiftReverse = @(ind,modul) mod_index(ind-(0:(modul-1)),modul);

for j = 1:3
    for i = (j+1):4
        i_symm = j;
        j_symm = i;
        
        Acoefs(1:num_of_quads,i_symm,j_symm) = Acoefs(shiftReverse(1,num_of_quads),i,j);
        B1coefs(1:num_of_quads,i_symm,j_symm) = B2coefs(shiftReverse(1,num_of_quads),i,j);
        B2coefs(1:num_of_quads,i_symm,j_symm) = B1coefs(shiftReverse(1,num_of_quads),i,j);
        Ccoefs(1:num_of_quads,i_symm,j_symm) = Ccoefs(shiftReverse(1,num_of_quads),i,j);
        
    end 
end


%i,j = 3,3
shifted_indices = @(ind,modul) mod_index((0:(modul-1)) + ind,modul);
% h_one coefs are already stored in 4,2
% h_two coefs are already stored in 4,3
% h_three = @(i) (1-2*c/3)*h_two(i) + h_one(i)*2*c/3;
h_three_coefs = @(ind,whichArray) (1-2*c/3)*whichArray(shifted_indices(ind,num_of_quads),4,3) + ...
    (2*c/3)*whichArray(shifted_indices(ind,num_of_quads),4,2);

%if m is odd
if(mod(num_of_quads,2) == 1 )
    for i = 1:num_of_quads
%         bezierPoints(:,3,3) = bezierPoints(:,3,3) ...
%             - ((-1)^i) * h_three(mod_index(i+ind-1,num_of_quads));
        Ccoefs(:,3,3) = Ccoefs(:,3,3) ...
            - ((-1)^i) * h_three_coefs(i+1,Ccoefs);
        B1coefs(:,3,3) = B1coefs(:,3,3) ...
            - ((-1)^i) * h_three_coefs(i+1,B1coefs);
        B2coefs(:,3,3) = B2coefs(:,3,3) ...
            - ((-1)^i) * h_three_coefs(i+1,B2coefs);
    end
else
    for i = 1:num_of_quads
%         bezierPoints(:,3,3) = bezierPoints(:,3,3) ...
%             - ((-1)^i) * (num_of_quads-i) * h_three(mod_index(i+ind-1,num_of_quads));
        Ccoefs(:,3,3) = Ccoefs(:,3,3) ...
            - ((-1)^i) * (num_of_quads-i) * h_three_coefs(i+1,Ccoefs)* 2/num_of_quads;
        B1coefs(:,3,3) = B1coefs(:,3,3) ...
            - ((-1)^i) * (num_of_quads-i) * h_three_coefs(i+1,B1coefs)* 2/num_of_quads;
        B2coefs(:,3,3) = B2coefs(:,3,3) ...
            - ((-1)^i) * (num_of_quads-i) * h_three_coefs(i+1,B2coefs)* 2/num_of_quads;
    end 
%     bezierPoints(:,3,3) = bezierPoints(:,3,3) * 2/num_of_quads;
end




end