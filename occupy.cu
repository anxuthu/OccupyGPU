#include <cuda.h>
#include <algorithm>

__device__ int get_global_index(void) {
	return blockIdx.x * blockDim.x + threadIdx.x;
}

__global__ void kernel(void) {
	while(1);
}

int main(int argc, char **argv) {
	int block_size = 128;
	int grid_size = 1;
	int gpu_num;

	unsigned long int bytes = 8e9; // size of memory to occupy
	float* data;

	cudaGetDeviceCount(&gpu_num);
	if (argc > 1) {
		for (int i = 1; i < argc; i++) {
			cudaSetDevice(atoi(argv[i]));
			cudaMalloc((void**)&data, bytes);
			kernel<<<grid_size, block_size>>>();
		}
	}
	else {
		for (int i = 0; i < gpu_num; i++) {
			cudaSetDevice(i);
			cudaMalloc((void**)&data, bytes);
			kernel<<<grid_size, block_size>>>();
		}
	}
	
	cudaDeviceSynchronize();

	return 0;
}
