import torch
import time

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if not torch.cuda.is_available():
    raise SystemExit("CUDA is not available. Stop here.")

device = torch.device("cuda")
print("GPU:", torch.cuda.get_device_name(0))

# Small GPU workload
x = torch.rand((8000, 8000), device=device)
y = torch.rand((8000, 8000), device=device)

torch.cuda.synchronize()
start = time.time()

z = torch.matmul(x, y)

torch.cuda.synchronize()
end = time.time()

print("Matrix multiplication completed on GPU.")
print("Result shape:", z.shape)
print("Time:", round(end - start, 4), "seconds")
print("GPU memory allocated:", round(torch.cuda.memory_allocated() / 1024**3, 2), "GB")
