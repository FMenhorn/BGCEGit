# B-Splines
Benni, 11.9.2015

## Short description
Here we implement the B-Spline basis functions. The provided functions can be used for getting the values of the i-th B-Spline basis functions of a certain degree, with a certain knot vector at arbitrary evaluation points.

## Example
The example just uses the functions for plotting all the BSpline-basis functions.

## Data Structures
The vectors [yy,xx] store the value of the i-th B-Spline basis function of degree n at the Evaluation point xx with the corresponding knot vector t. $ yy=N_{i,p}\left(xx\right) $

## Theory and References
The B-Spline basis functions are needed for the definition of NURBS curves as well as surfaces. For an explanation of the terms knot vector, degree and what the i-th function is, see section "2.4.2 NURBS basis functions" in "GoogleDrive:TUM BGCE master folder/Presentations and Reports/FirstMilestone".


