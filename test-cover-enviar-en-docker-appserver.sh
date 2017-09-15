ls -a
ls shared -a
nosetests --with-coverage && \
coverage xml && \
mv coverage.xml shared/coverage.xml && \
ls -a