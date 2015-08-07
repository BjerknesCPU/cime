# Macros for finding static libraries
macro (find_static_library)
    set (_CMAKE_FIND_LIBRARY_SUFFIXES ${CMAKE_FIND_LIBRARY_SUFFIXES})
    if ("${CMAKE_SYSTEM_NAME}" STREQUAL "Windows")
        set (CMAKE_FIND_LIBRARY_SUFFIXES ".lib")
    else ()
        set (CMAKE_FIND_LIBRARY_SUFFIXES ".a")
    endif ()
    find_library(${ARGN})
    set (CMAKE_FIND_LIBRARY_SUFFIXES ${_CMAKE_FIND_LIBRARY_SUFFIXES})
endmacro ()