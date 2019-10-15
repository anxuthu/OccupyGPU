# OccupyGPU

This code occupies a gpu's utils at 100% and approx. 8GB memory.

Occupy all gpus in default:

```
nvcc ./occupy.cu -o run && ./run &
```

To occupy specific gpus, 0 and 2 for example:

```
nvcc ./occupy.cu -o run && ./run 0 2 &
```

nvcc is the CUDA complier, which usually comes along with the cuda-x.x folder when you install CUDA into the system diretories. For now, there is no nvcc if you only install the cudatoolkit package from anaconda.
