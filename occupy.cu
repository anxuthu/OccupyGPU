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

	cudaGetDeviceCount(&gpu_num);
	if (argc > 1) {
		for (int i = 1; i < argc; i++) {
			cudaSetDevice(atoi(argv[i]));
			kernel<<<grid_size, block_size>>>();
		}
	}
	else {
		for (int i = 0; i < gpu_num; i++) {
			cudaSetDevice(i);
			kernel<<<grid_size, block_size>>>();
		}
	}
	if (argc > 1) {
		grid_size = atoi(argv[1]);
	}
	
	cudaDeviceSynchronize();

	return 0;
}
