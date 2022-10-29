# Install script for directory: /home/hammer/Desktop/pythonProjects/pytech/lzo-2.10

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/share/doc/lzo/AUTHORS;/usr/local/share/doc/lzo/COPYING;/usr/local/share/doc/lzo/NEWS;/usr/local/share/doc/lzo/THANKS;/usr/local/share/doc/lzo/LZO.FAQ;/usr/local/share/doc/lzo/LZO.TXT;/usr/local/share/doc/lzo/LZOAPI.TXT")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/share/doc/lzo" TYPE FILE FILES
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/AUTHORS"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/COPYING"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/NEWS"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/THANKS"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/doc/LZO.FAQ"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/doc/LZO.TXT"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/doc/LZOAPI.TXT"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/include/lzo/lzo1.h;/usr/local/include/lzo/lzo1a.h;/usr/local/include/lzo/lzo1b.h;/usr/local/include/lzo/lzo1c.h;/usr/local/include/lzo/lzo1f.h;/usr/local/include/lzo/lzo1x.h;/usr/local/include/lzo/lzo1y.h;/usr/local/include/lzo/lzo1z.h;/usr/local/include/lzo/lzo2a.h;/usr/local/include/lzo/lzo_asm.h;/usr/local/include/lzo/lzoconf.h;/usr/local/include/lzo/lzodefs.h;/usr/local/include/lzo/lzoutil.h")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/include/lzo" TYPE FILE FILES
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1a.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1b.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1c.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1f.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1x.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1y.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo1z.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo2a.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzo_asm.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzoconf.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzodefs.h"
    "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/include/lzo/lzoutil.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/lib/liblzo2.a")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/lib" TYPE STATIC_LIBRARY FILES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/liblzo2.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzopack" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzopack")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzopack"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/libexec/lzo/examples/lzopack")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/libexec/lzo/examples" TYPE EXECUTABLE FILES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/lzopack")
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzopack" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzopack")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzopack")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzotest" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzotest")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzotest"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/libexec/lzo/examples/lzotest")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/libexec/lzo/examples" TYPE EXECUTABLE FILES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/lzotest")
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzotest" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzotest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/lzotest")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/simple" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/simple")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/simple"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/libexec/lzo/examples/simple")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/libexec/lzo/examples" TYPE EXECUTABLE FILES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/simple")
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/simple" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/simple")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/simple")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/testmini" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/testmini")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/testmini"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/libexec/lzo/examples/testmini")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/libexec/lzo/examples" TYPE EXECUTABLE FILES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/testmini")
  if(EXISTS "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/testmini" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/testmini")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/usr/local/libexec/lzo/examples/testmini")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/lib/pkgconfig/lzo2.pc")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/lib/pkgconfig" TYPE FILE FILES "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/lzo2.pc")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/hammer/Desktop/pythonProjects/pytech/lzo-2.10/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
