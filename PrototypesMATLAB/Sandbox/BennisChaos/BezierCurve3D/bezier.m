function [x,y,z] = bezier(P,h)
% BEZIER Returns x,y,z values of a 3D bezier-curve with the given control points P and
% stepwidth h

t=0:h:1;

N_t=numel(t);
x=zeros(1,N_t);
y=zeros(1,N_t);
z=zeros(1,N_t);

n=size(P,2)-1;

for i = 0:n
    x=x+bernstein(i,n,t)*P(1,i+1);
    y=y+bernstein(i,n,t)*P(2,i+1);
    z=z+bernstein(i,n,t)*P(3,i+1);
end

end