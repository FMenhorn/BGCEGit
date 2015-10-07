#MATLAB prototypes
Here every kind of MATLAB code relevant for the BGCE Project is stored. Please follow the "MATLAB prototype etiquette" when saving something to PrototypesMATLAB. If you don't want to follow those rules use the Sandbox instead.

##Existing and non-existing prototypes

###Basic Math Algorithms
- [x] B-Spline basis function evaluation

###Algorithms
- [ ] Marching Cubes (would be useful for trying out stuff and comparison to Dual Contouring)
- [ ] Dual Contouring (would be useful for trying out stuff and comparison to Marching Cubes)
- [ ] Iterative Parameter Fitting (Already existing in Sandbox)

###Big Tasks
- [ ] manual NURBS Fitting Pipeline
- [ ] automatic NURBS Fitting Pipeline

##MATLAB prototype etiquette
Store all necessary data in git/PrototypesMATLAB
If you are coding something and it is not agreeing with these rules, please use git/PrototypesMATLAB/Sandbox

### Relevance
Is the prototype relevant?
* important basic algorithms e.g. Bernstein polynomial, NURBS implementation in 1D/2D, marching cubes... 
* every more or less complex algorithm which helps others to save time is relevant!

### Readme
Provide a README.md on the top level of the folder which holds your prototype
* Use the provided sceleton "sceletonREADME"
* Write the name of the author and the date of publication in the README
* Short description of what the prototype does and what it is useful for
* Give references for the theory. Provide pdf references in Google Drive "TUM BGCE master folder/References". Give link to online references. The whole theory should be understandable from the README and the given References.
* Explain uncommon datastructures (e.g. How do I store patches? How do I define boundary conditions?)

### Example
Provide a working example with name (example.m)
* should illustrates how to use your code
* what it does... (if possible with visualization!)
* in README explain what happens 
* explain the use of datastructures

### Formulas
Use formulas where necessary. Write them down in Latex, eventhough git cannot render it, it may be useful later.

### Style
* Do not copy other functions of the prototype section! 
* Use them by properly referencing them! 
* Reuse existing code if possible!
* Give unique names!
