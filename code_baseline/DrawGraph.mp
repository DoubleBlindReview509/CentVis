verbatimtex
%&latex
\documentclass{article}
\usepackage{amsfonts}
\usepackage{bm}
\usepackage{amsmath}
\begin{document}
etex

prologues:=3;
filenametemplate "%j-%c.eps";
u=1mm;

def ds(expr x, s, c) =
	draw fullcircle scaled s shifted x withcolor c;
enddef;

def dp(expr x, s, c) =
	fill fullcircle scaled s shifted x withcolor c;
	draw fullcircle scaled s shifted x withcolor black;
enddef;

vardef COL(expr r, g, b) = ((r/255)*red + (g/255)*green + (b/255)*blue) enddef;

vardef getcol(expr xx) =
	save x, y;
	numeric x, y;
	x := xx;
	y := 1-x;
	if x>y :
		y := y / x;
		x := 1.0;
	else :
		x := x / y;
		y := 1.0;
	fi;
	(x*green + y*red)
enddef;

beginfig(1);

pickup pencircle scaled 1.05;

color nodeColor;
nodeColor := green;

numeric N, M;
N := scantokens(readfrom "../log/GraphInformation.txt");
M := scantokens(readfrom "../log/GraphInformation.txt");
closefrom "../log/GraphInformation.txt";

numeric len, r;
len := 10u;
r := 4u;

numeric p[][];
for i = 1 upto N :
	p[i][1] := scantokens(readfrom "../log/NodePos.txt") * len;
	p[i][2] := scantokens(readfrom "../log/NodePos.txt") * len;
endfor;
closefrom "../log/NodePos.txt";

string lab[];
for i = 1 upto N :
	lab[i] := (readfrom "../log/NodeLabels.txt");
endfor;
closefrom "../log/NodeLabels.txt";

numeric ux, uy, vx, vy;
pickup pencircle scaled 1.05;

for i = 1 upto M :
	ux := scantokens(readfrom "../log/Edges.txt") * len;
	uy := scantokens(readfrom "../log/Edges.txt") * len;
	vx := scantokens(readfrom "../log/Edges.txt") * len;
	vy := scantokens(readfrom "../log/Edges.txt") * len;
	draw (ux, uy)--(vx, vy);
endfor;
closefrom "../log/Edges.txt";

numeric rank[];
for i = 1 upto N :
	rank[i] := scantokens(readfrom "../log/NodeRank.txt");
endfor;
closefrom "../log/NodeRank.txt";

for i = 1 upto N :
	dp((p[i][1], p[i][2]), r, getcol(rank[i]));
	label(lab[i] infont defaultfont scaled sqrt(1/length(lab[i])), (p[i][1], p[i][2]));
endfor;

endfig;

end;
