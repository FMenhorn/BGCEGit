function handle = petersPlot(points,stepsize)

%% Peter's scheme plot
% Plot of a mesh using peter's scheme

m = size(points,2);
n = size(points,3);

handle = figure('Name', 'Peters plot');
plotPoints(points);
hold on

for j = 2:(n-1)
    for i = 2:(m-1)
        neighbours = points(:,(i-1):(i+1),(j-1):(j+1));
        bezierPoints = getBiquadraticPatch(neighbours);
        plotPoints(bezierPoints);
        [x,y,z] = bezier(bezierPoints,stepsize);
        surf(x,y,z);
    end
end