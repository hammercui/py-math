# CMake generated Testfile for 
# Source directory: /home/hammer/Desktop/pythonProjects/pytech/lzo-2.10
# Build directory: /home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(simple "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/simple")
set_tests_properties(simple PROPERTIES  _BACKTRACE_TRIPLES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;254;add_test;/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;0;")
add_test(testmini "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/testmini")
set_tests_properties(testmini PROPERTIES  _BACKTRACE_TRIPLES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;255;add_test;/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;0;")
add_test(lzotest-01 "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/lzotest" "-mlzo" "-n2" "-q" "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/COPYING")
set_tests_properties(lzotest-01 PROPERTIES  _BACKTRACE_TRIPLES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;256;add_test;/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;0;")
add_test(lzotest-02 "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/lzotest" "-mavail" "-n10" "-q" "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/COPYING")
set_tests_properties(lzotest-02 PROPERTIES  _BACKTRACE_TRIPLES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;257;add_test;/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;0;")
add_test(lzotest-03 "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/lzotest" "-mall" "-n10" "-q" "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzodefs.h")
set_tests_properties(lzotest-03 PROPERTIES  _BACKTRACE_TRIPLES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;258;add_test;/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/CMakeLists.txt;0;")
