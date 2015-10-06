function [ TX,TY,TZ ] = Bilinear(Px,Py,Pz)
%TRIANGLE Summary of this function goes here
%   Detailed explanation goes here

%number of gridpoints, does this help?
Nu = size(Px,2); %gridpoints in u direction
Nv = size(Px,1); %gridpoints in v direction

%how to iterate over triangles?
%what is Tmin, Tmax?
hu = 1/(Nu-1);
hv = 1/(Nv-1);

for iu = 1:Nu-1
    for jv = 1:Nv-1
        
        A=[Px(jv,iu),Py(jv,iu),Pz(jv,iu)]';
        B=[Px(jv,iu+1),Py(jv,iu+1),Pz(jv,iu+1)]';
        C=[Px(jv+1,iu),Py(jv+1,iu),Pz(jv+1,iu)]';
        D=[Px(jv+1,iu+1),Py(jv+1,iu+1),Pz(jv+1,iu+1)]';       
        AB=B-A;
        AC=C-A;
        DB=B-D;
        DC=C-D;
        
        uT=@(u)(u/hu-(iu-1));
        vT=@(v)(v/hv-(jv-1));
        
        %bilinear
        T=@(u,v,d)...
            (1-uT(u)).*(1-vT(v)).*A(d)+...
            (1-vT(v)).*uT(u).*B(d)+...
            (1-uT(u)).*vT(v).*C(d)+...
            uT(u).*vT(v).*D(d);
        
        %linear
%         T=@(u,v,d)  heaviside(1-Tu(u)-Tv(v)).*(...
%             A(d)+AB(d).*Tu(u)+AC(d).*Tv(v)...
%             )+...
%             heaviside(-1+Tu(u)+Tv(v)).*(...
%             D(d)+DB(d).*(1-Tv(v))+DC(d).*(1-Tu(u))...
%             );
        
        [U,V]=meshgrid((iu-1)*hu:hu/10:iu*hu,(jv-1)*hv:hv/10:jv*hv);
        TX((jv-1)*10+1:jv*10+1,(iu-1)*10+1:iu*10+1)=T(U,V,1);
        TY((jv-1)*10+1:jv*10+1,(iu-1)*10+1:iu*10+1)=T(U,V,2);
        TZ((jv-1)*10+1:jv*10+1,(iu-1)*10+1:iu*10+1)=T(U,V,3);
    end
end




end

