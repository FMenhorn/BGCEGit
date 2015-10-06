function y = d_bspline_basis_recurrence(j,n,t,x)

y = zeros(size(x));
if n > 1
    b = bspline_basis(j,n-1,t,x);
    d_b = d_bspline_basis(j,n-1,t,x);
    dn = b + (x-t(j+1)).*d_b;    
    dd = t(j+n) - t(j+1);
    if dd ~= 0  % indeterminate forms 0/0 are deemed to be zero
        y = y + (dn./dd);
    end
    b = bspline_basis(j+1,n-1,t,x);
    d_b = d_bspline_basis(j+1,n-1,t,x);
    dn = (t(j+n+1) - x).*d_b - b;
    dd = t(j+n+1) - t(j+1+1);
    if dd ~= 0
        y = y + (dn./dd);
    end
else
    y(:)=0;
end

end