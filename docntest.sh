echo '\033[0;34m'
echo '############################'
echo '####    DOCUMENTACION   ####'
echo '############################'
echo
doxygen documentacion/doxygen.config
echo
echo '############################'
echo '###  FIN DOCUMENTACION   ###'
echo '############################'
echo
echo '\033[1;33m'
echo '############################'
echo '#######     TESTS    #######'
echo '############################'
echo
nosetests -x -v
echo
echo '############################'
echo '#####     FIN TESTS    #####'
echo '############################'
