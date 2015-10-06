function [ x,dx ] = reparametrize( D,B,x,t,n )
%REPARAMETRIZE calculates the correction for the parametrization due to the
%rules presented in RogersFog1989
% D:    difference of original datapoints and corresponding points on
%       Bspline, D=P-P_c
% B:    control points of the Bspline
% x:    parameters
% t:    knot vector
% n:    degree of the Bspline (n=3 quadratic...)
%returns
% x:    corrected parameters
% dx:   parameter correction (unsure about correction sign...)

tol = 10^-10;
itmax = 3;

it = 0;
dx = inf;

while(mean(dx)>tol && it < itmax)
    N=size(D,1);
    dx=zeros(N,1);
    for i = 2:N-1
        xold = x(i);
        [d_Nx,d_Ny,d_Nz] = d_NURBS(B,xold,t,n);
        d_N=[d_Nx,d_Ny,d_Nz]';
        denom=(d_N'*d_N);
        %
        if(denom ~= 0)
            dx(i) = (D(i,:)*d_N)/denom;
        end
        xnew=xold+dx(i);
        if(xnew<0 || xnew>1)
            x(i)=xold;
        else
            x(i)=xnew;
        end
    end
    it = it+1;
end

if(it == itmax)
    warning('no convergence in reparametrization!');
else
    disp(sprintf('convergence after %d iterations.',it));
end

end

