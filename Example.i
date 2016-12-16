c HPGe Crystal from Detective 200 with Radium-226
c 85mm D x 30mm T P-type Germanium Crystal
c --------------------------------------
c Cell Card
c ---------------------------------------
1    2 -0.001205 1 -2 -3 #2 #3 #4 #5 #6 #7 #8 IMP:P=1 $ AIR
2    4 -2.698  -2 -13 15 #(16 -14 -17)        IMP:P=1 $ Aluminum Housing
3    4 -2.698  -17 21 -22 23 #4 #5 #6 #7 #8   IMP:P=1 $ Crystal Holder
4    5 -5.323  21 -23 32 -33 #5 #6 #7 #8      IMP:P=1 $ Outer Electrode
5    5 -5.323  21 -31 -32                     IMP:P=1 $ Window Electrode
6    5 -5.323  -32 31 -33 #(-41 42 -33) #7 #8 IMP:P=1 $ HPGe Crystal
7    0  (42 -41 -33 43):(33 -23 -17) #8       IMP:P=0 $ Vacuum Well
8    6 -8.96 -43 42 -17                       IMP:P=1 $ Central Finger
99   0 -1:3:2                                 IMP:P=0 $ Void Outside

c ---------------------------------------
c Surface Card
c      0# = Sim Space
c      1# = Housing Space
c      2# = Inner Space
c      3# = Crystal Space
c      4# = Cold Finger Space
c ---------------------------------------
1    PX -5.0     $ Back of Sim Space
2    PX 38       $ Front of Sim Space
3    CX 10.0     $ Radius of Sim Space
13   CX 7.20     $ Outer radius of Detector Housing
14   CX 7.05     $ Inner radius of Detector Housing
15   PX 30.0     $ Front of Detector Housing
16   PX 30.15    $ Front/Inside of Detector Housing
17   PX 35.20    $ Back of Vacuum Well Inside Detector Housing
21   PX 31.5     $ Front of Window Electrode
22   CX 4.40     $ Outside of Crystal Holder
23   CX 4.25     $ Outer Electrode Radius
31   PX 31.57    $ Front of HPGe Behind Window
32   CX 4.18     $ Crystal Radius
33   PX 34.50    $ Back of HPGe
41   CX 0.33     $ Core Hole in Ge Radius
42   PX 34.00    $ Front of Core Hole
43   CX 0.3      $ Finger Radius 

c ---------------------------------------
c Material Card
c ----------------------------------------
m2   6000  -0.000124 $ Dry Air ICRU
     7000  -0.755268
     8000  -0.231781
     18000 -0.012827 
m4   13000 -1        $ Aluminium
m5   32000 -1        $ Pure Germanium Crystal
m6   29000 -1        $ Copper
c ---------------------------------------
c Source Terms
c ---------------------------------------
mode P
phys:P,E 
nps 6e8
sdef POS=0 0 0  erg=D2 PAR=2 DIR=D1 VEC=1 0 0                    
si1    0.8 1.0                                                         
sp1    0.0 1.0
si2  L .186211 .241997 .295224 .351932 .609312 .768356 1.120287 1.123811
       1.377669 1.729595 1.764494 1.84742 2.20421
sp2    0.024278697 0.050815877 0.120264243 0.225848343 0.260290215
       0.027666422 0.086386991 0.033877251 0.022584834 0.016656315
       0.089774716 0.012195811 0.029360285
f8:P 6
f18:P 6
ft18 GEB 0.00073568688 0.00085954495 0.28984239
e0    0.0 8000I 2.4
e8    0.0 8000I 2.4
e18   0.0 8000I 2.4
