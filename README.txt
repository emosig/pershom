Extended Pareto Grid Calculator

The main program is EPG.py, it is a GUI, where one can insert the function, calculate the EPG using different tolerances;
each time one changes the initial parameters a new tab will open in the notebook at the click.

The initial parameters are:

	- the function f:
	 one have to insert the two components, f1 and f2, as polinomial strings made of monomials of the form
	 r cos^a(bx+c)sen^d(ex+f)cos^g(hy+i)sen^j(ky+l) with a,b,c,d,e,f,g,h,i,j,k,l integer numbers, a,d,g,j>0
	
	- the number p of points in a row of the grid on the flat torus: 
	the program will work on an equally-spaced grid on the torus made of p*p points
	
	- tolerance:
	this tolerance will be used in the part of the algorithm where it is checked if a point of the grid is Pareto critical; the condition
	on the determinant of the Jacobian of f to be 0, is replaced by the condition that check if the absolute value of the Jacobian is lower then 
	the tolerance.
	
After one plot the EPG, there is the possibility to:

	- save the points of the EPG on a .txt file

	- reduce the noise using an algotithm that intersect the EPG with a sheaf of parallels lines, as thik as the parameter Line Tolerance, and
	recalculate the condition to be Pareto critical on points of the line that are sufficently near to each other and that span a sufficently big
	interval in their abscissa.
	
	-after that one can also save on a .txt file the points of the new EPG
	