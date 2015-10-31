
cmake_minimum_required(VERSION 2.8)

PROJECT(WorkUnstructuredGrid)

find_package(VTK REQUIRED)
include(${VTK_USE_FILE})

add_executable(WorkUnstructuredGrid MACOSX_BUNDLE WorkUnstructuredGrid)

if(VTK_LIBRARIES)
  target_link_libraries(WorkUnstructuredGrid ${VTK_LIBRARIES})
else()
  target_link_libraries(WorkUnstructuredGrid vtkHybrid vtkWidgets)
endif()
