cmake_minimum_required(VERSION 3.13)
project(opensslqt5 LANGUAGES C)

configure_file("${CMAKE_SOURCE_DIR}/scripts/generatesource.py" "${CMAKE_BINARY_DIR}/scripts/generatesource.py" COPYONLY)
configure_file("${CMAKE_SOURCE_DIR}/scripts/symbols_ssl.txt" "${CMAKE_BINARY_DIR}/scripts/symbols_ssl.txt" COPYONLY)
configure_file("${CMAKE_SOURCE_DIR}/scripts/symbols_crypto.txt" "${CMAKE_BINARY_DIR}/scripts/symbols_crypto.txt" COPYONLY)
configure_file("${CMAKE_SOURCE_DIR}/src/.gitkeep" "${CMAKE_BINARY_DIR}/src/.gitkeep" COPYONLY)

add_custom_command(
  OUTPUT "${CMAKE_BINARY_DIR}/src/libopensslqt5.c" "${CMAKE_BINARY_DIR}/src/libopensslqt5.map"
  COMMAND "${CMAKE_BINARY_DIR}/scripts/generatesource.py"
  DEPENDS "${CMAKE_BINARY_DIR}/scripts/generatesource.py"
)

add_library(opensslqt5 SHARED "${CMAKE_BINARY_DIR}/src/libopensslqt5.c")
target_link_libraries(opensslqt5
  PUBLIC
  -Wl,--no-undefined
  "-Wl,--version-script,${CMAKE_BINARY_DIR}/src/libopensslqt5.map"
  ${CMAKE_DL_LIBS}
)
install(TARGETS opensslqt5 DESTINATION lib)
