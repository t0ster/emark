About
=====

Electronic mark sheet and time table.

.. image:: http://dl.dropbox.com/u/407968/Image/Screen%20shot%202011-06-19%20at%2022.38.44.png

Runing in dev env
=================


::

	git clone git://github.com/t0ster/emark.git
	cd emark
	python bootstrap.py
	./bin/buildout -c dev.cfg
	./bin/django syncdb
	./bin/django migrate
	./bin/runserver

Go to http://localhost:8000
