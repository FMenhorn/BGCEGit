function y = bspline_basis_recurrence(j,n,t,x)

y = zeros(size(x));
if n > 1
    b = bspline_basis(j,n-1,t,x);
    dn = x - t(j+1);
    dd = t(j+n) - t(j+1);
    if dd ~= 0  % indeterminate forms 0/0 are deemed to be zero
        y = y + b.*(dn./dd);
    end
    b = bspline_basis(j+1,n-1,t,x);
    dn = t(j+n+1) - x;
    dd = t(j+n+1) - t(j+1+1);
    if dd ~= 0
        y = y + b.*(dn./dd);
    end
elseif t(j+2) < t(end)  % treat last element of knot vector as a special case
	y(t(j+1) <= x & x < t(j+2)) = 1;
else
	y(t(j+1) <= x) = 1;
end