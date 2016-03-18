all: release

release:
	mkdir -p build	
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j4 VERBOSE=1
	
debug:
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Debug .. && make -j4 VERBOSE=1

clean:
	cd build && rm -rf CMakeFiles/CADToVoxel.dir/Voxelizer/*.o CMakeFiles/CADToVoxel.dir/Reader/*.o CMakeFiles/CADToVoxel.dir/Writer/*.o
