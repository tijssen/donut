
donut.py
===
A spinning donut for your terminal, written in Python.

Full disclosure: I was first inspired to write this program by a video by Lex Fridman [1], which led me to the excellent article written by Andy Sloane [2].
I highly recommend you have a look at both of them.

I wrote this project just for fun, it doesn't have any practical purpose besides education.
There exist other Python implementations of this problem, such as [3].
However, what makes this one unique is that it uses NumPy to accelerate the computations, resulting in a better framerate for the animation.

Usage
---
	git clone https://github.com/tijssen/donut
	cd donut
	python3 donut.py

You can also uncomment the last part of the code to see a visualization of the data points in three dimensions using matplotlib.

To-do
---
I know that the code isn't ideal, there is still room for optimization.
For instance, we could remove the SciPy dependency, remove for-loops and clean up the code.
I will work on the code as my interest permits.
If you know how to do it better, feel free to submit a pull request!

Sources
---
[1] Fridman, Lex (2020). Donut-shaped C code that generates a 3D spinning donut, <https://youtu.be/DEqXNfs_HhY>.

[2] Sloane, Andy (2011). Donut math: how donut.c works, <https://www.a1k0n.net/2011/07/20/donut-math.html>.

[3] <https://github.com/RandomThings23/donut>.

Copyright
---
Copyright (C) 2021, 2022 Luuk Tijssen

License: Creative Commons 0 (public domain software).
