function [v,f,ff] = torus(xy,z,hpr,dev)

% TORUS  Returns Faces and Vertices of a Torus
%
% [V,F,FF] = TORUS(XY,DZ,POS,HPR)
%
%--------------------------------------------------------
%
% XY  = [ N by 2 by 1 ] - [ X Y ]  2 Columns for XY-Face
%       [ N by 2 by 2 ] - [ X(Z1/Z2) Y(Z1/Z2) ]  2 XY-Faces
%
% DZ  = High of Torus - single Element --> Z1=0; Z2=DZ
%       [ Z1  Z2 ]    - Two Elements
%       [ N by 2 ]    - Curve for 2 Faces
%
%
% HPR = [ Heading  Pitch  Roll ]  Pitch: positive down
%
% DEV = [ DX DY DZ ] Deviation of Torus
%
%
%--------------------------------------------------------
%
%  V    XYZ-Coordinates of Vertices
%
%  F    VerticeIndex for Faces of TORUS
%
%  FF   VerticeIndex for Faces of XY-Plain
%
%
%--------------------------------------------------------
% Example:
%
% p = linspace(0,2*pi,17); p = p(:);
% xy = 10 * [sin(p) cos(p)];
% dz = [sin(2*p)-2 cos(2*p)+2]
% [v,f,ff] = torus(xy,dz);
%
%  figure;
%  axes( 'dataaspectratio' , [ 1  1  1 ] , ...
%        'view'            , [ -30  15 ] , ...
%        'nextplot'        , 'add'  );
% 
%  patch(     'vertices' , v    , ...
%                'faces' , f    , ...
%            'facecolor' , 'r'  , ...
%            'edgecolor' , 'k'          )
% 
%  patch(     'vertices' , v       , ...
%                'faces' , ff(1,:) , ...
%            'facecolor' , 'c'     , ...
%            'edgecolor' , 'k'          )
% 
%  patch(     'vertices' , v+ ones(size(v,1),1)*[0 0 5] , ...
%                'faces' , ff(2,:) , ...
%            'facecolor' , 'm'     , ...
%            'edgecolor' , 'k'          )
% 
% legend('Torus','Bottom','Top+5')
%
%--------------------------------------------------------
%
% see also: TUBUS, CORPUS, GLIDER, HEPIRO, PATCH
%

Nin = nargin;

Nout = nargout;

if Nin < 2, error('Not enough Input Arguments'); end
if Nin < 3, hpr = []; end
if Nin < 4, dev = []; end

%--------------------------------------------------------------
% Basic Check of Inputs

msg = cell(0,1);

si = size(xy);
s3 = size(xy,3);

if ~( isnumeric(xy) & ( prod(si) == si(1)*si(2)*s3 ) & ...
      ( si(1) >= 3 ) & ( si(2) == 2 ) & any( s3 == [1 2] ) )
    msg = cat(1,msg,{'XY must have 2 Columns and more than 2 Rows.'});
elseif s3 == 1
    xy = xy(:,:,[1 1 ]);
end

sz = size(z); pz = prod(sz);

if ~( isnumeric(z) & ( isequal(sz,si([1 2])) | any( pz == [ 1  2 ] ) ) )
    msg = cat(1,msg,{'DZ must have 1, 2 or Elements as XY.'});
elseif pz == 1
    z = ones(si(1),1) * [ 0  z ];
elseif pz == 2
    z = ones(si(1),1) * z(:)';
end   

for v = { hpr dev }
    ok = isempty(v{1});
    if ~ok
        ok = ( isnumeric(v{1}) & ( prod(size(v{1})) <= 3 ) );
        if ok
           ok = all(isfinite(v{1}));
        end
    end
    if ~ok
        break
    end
end

if ~ok
    msg = cat(1,msg,{'Inputs POS and HPR must be finite numeric with max. 3 Elements.'});
end


if ~isempty(msg)
    msg = sprintf('%s\n',msg{:});
    error(sprintf('Invalid Inputs.\n%s',msg));
end

%--------------------------------------------------------------

if isempty(dev)
   dev = [ 0  0  0 ];
elseif prod(size(dev)) < 3
   dev = cat(2,dev(:)',0,0);
   dev = dev(1:3);
end

if isempty(hpr)
   hpr = [ 0  0  0 ];
elseif prod(size(pos)) < 3
   hpr = cat(1,hpr(:),0,0);
   hpr = hpr(1:3);
end

%--------------------------------------------------------------

v = cat( 2 , xy , permute(z,[1 3 2]) ); %%% [ N by 3 by 2 ]

m = size(v,1);

n = m - 1;

f = zeros(n,4);

f(:,1) = ( 1 : n )';
f(:,2) = f(:,1) + 1;
f(:,3) = f(:,2) + m;
f(:,4) = f(:,3) - 1;

v = cat( 1 , v(:,:,1) , v(:,:,2) );

ff = cat( 1 , ( 1 : m ) , ( 1 : m ) + m );

%--------------------------------------------------------------
% Rotation and Deviation

if ~all( hpr == 0 )  % Subfunction see below
    [v(:,1),v(:,2),v(:,3)] = hepirot(v(:,1),v(:,2),v(:,3),hpr);
end

v = v + dev(ones(1,2*m),:);

%--------------------------------------------------------------
% Plot

if Nout == 0

   lim = cat( 1 , min(v,[],1) , max(v,[],1) );
   lim = permute( lim  , [ 2 1 ] );
   dlm = diff(lim,1,2);
   dlm = dlm + ( dlm == 0 );
   lim = lim + dlm/4 * [ -1  1 ];

   figure
   axes( 'xlim' , lim(1,:) , ...
         'ylim' , lim(2,:) , ...
         'zlim' , lim(3,:) , ...
         'dataaspectratio' , [1 1 1] , ...
         'nextplot' , 'add' , ...
         'view'     , [20 30] );
   patch('vertices',v,'faces',f)

   if sqrt(sum((v(1+[0 m],[1 2])-v(m+[0 m],[1 2])).^2,2)) ...
      <= 1e-3 * max(diff(lim([1 2],:),1,2))
      patch('vertices',v,'faces',ff)
   end
        
   clear v f ff

end

%***************************************************************
%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

function [x,y,z] = hepirot(x,y,z,v);

% HEPIRO   Rotates XYZ-Coordinates by Heading, Pitch and Roll
%
% [ X , Y , Z ] = HEPIRO( X , Y , Z , HPR )
%
% HPR = [ Heading Pitch Roll ]
%
% Heading  Rotation around Z-Axis
% Pitch    Rotation around Y-Axis
% Roll     Rotation around X-Axis
%
%--------------------------------------------------------
% Example with GLIDER:
%
% [v,f,d,m] = glider;
%
% [x,y,z] = hepiro(v(:,1),v(:,2),v(:,3),[-40 30 20]);
%
% figure('ColorMap',m);
%
% axes( 'dataaspectratio' , [ 1  1  1 ] , ...
%       'view'            , [ -30  30 ] , ...
%       'nextplot'        , 'add'  );
%
% patch(     'vertices' , [ x y z ] , ...
%               'faces' , f         , ...
%     'facevertexcdata' , d         , ...
%        'cdatamapping' , 'direct'  , ...
%           'facecolor' , 'flat'    , ...
%           'edgecolor' , 'none'          )
%
% h = light('style','infinite','color','w');
%
% lightangle(h,60,60)
%

Nin = nargin;

if Nin < 3
   error('X, Y and Z required.');
end

%**********************************************************************
% Check Inputs

msg = cell(0,1);

%---------------------------------------------------------------------
% XYZ

if ~( isnumeric(x) & isnumeric(y) & isnumeric(z) )
    msg = cat(1,msg,{'X, Y and Z must be numeric.'});
end

sz = size(z);

if ~isequal(size(x),size(y),sz)
    msg = cat(1,msg,{'Size of X, Y and Z must be agree.'});
end

%---------------------------------------------------------------------
% HPR

if Nin < 4
   v = [];
end

ok = isnumeric(v);
if ok
   p  = prod(size(v));
   ok = ( p <= 3 );
   if ok & ~isempty(v)
      v = cat( 1 , v(:) , zeros(3-p,1) );
   elseif ~ok
      msg = cat(1,msg,{'HPR must be numeric with max. 3 Elements.'});
   end
end

%---------------------------------------------------------------------

if ~isempty(msg)
    msg = sprintf('%s\n',msg{:});
    msg = sprintf('Invalid Inputs.\n%s',msg);
    error(msg);
end

if isempty(v)
   return
end

%**********************************************************************

v = v - 360 * floor( v / 360 );   % [ 0 .. 360 )

if all( v == 0 )
   return
end

v = v * pi/180;

sv = sin(v);
cv = cos(v);

ex = [ 1  0  0 ];
ey = [ 0  1  0 ];
ez = [ 0  0  1 ];

T = cat( 1 , ex , ey , ez );

%*********************************************
% Zyclic Permutation: ZXY / YZX / XYZ
%------------------------------------------
% Head around Z
%    w = [  cv(1)  sv(1)  0
%          -sv(1)  cv(1)  0
%            0      0     1 ];
%    T = w * T;
%------------------------------------------
% Pitch around Y
%    w = [ cv(2)  0  -sv(2)
%           0     1    0   
%          sv(2)  0   cv(2) ];
%    T = w * T;
%------------------------------------------
% Roll around X
%    w = [  1     0     0   
%           0   cv(3)  sv(3)
%           0  -sv(3)  cv(3) ];
%    T = w * T;
%*********************************************

for ii = 1 : 3

    if ~( v(ii) == 0 )

        w = [  cv(ii)  sv(ii)  0
              -sv(ii)  cv(ii)  0
                0       0      1 ];

        jj = ( 1 : 3 ) - 1 + ii;     % Zyclic Index
        jj = jj - 3 * floor(jj/3);
        jj = jj + 3 * ( jj == 0 );
        
        T = w(jj,jj) * T;

    end

end

% Check for valid RotationMatrice
% d = inv(T) - T'; max(abs(d(:)))  % must be ZERO

%------------------------------------------
% Transformation

xyz = cat(2,x(:),y(:),z(:));

xyz = xyz * T;

%------------------------------------------
% Reshape back

x = reshape(xyz(:,1),sz);
y = reshape(xyz(:,2),sz);
z = reshape(xyz(:,3),sz);

%***************************************************************
%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

function p = comb(n,k)

if any( k == [ 0  1  n ] )

   if     k == 0
      p = zeros(1,0);
   elseif k == 1
      p = ( 1 : n )';
   else
      p = ( 1 : k );
   end   

   return

end

%------------------------------------------------------

m = nok(n,k);

p = zeros(m,k);

z = 0;

for ii = 1 : n-1
 
     m = nok(n-ii,k-1);
    jj = z + (1:m);

    p(jj,1) = ii;
    p(jj,2:k) = comb(n-ii,k-1) + ii;

     z = z + m;

end

%******************************************************
%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

function n = nok(n,k)

n = prod(n-k+1:n) / prod(1:k);
