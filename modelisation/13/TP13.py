import numpy as np 
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

img = cv2.imread(CURRENT_DIR.joinpath("test_image.jpg"))
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img_rgb)
# plt.show()

img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(img_grey, cmap='grey')
# plt.show()

A = np.array(img, dtype=float) / 255.0

# A = np.array([[1,2,3],[0,1,2]], dtype = float)
# U,S,Vt = np.linalg.svd(A,full_matrices = False)
# 
# print(U@np.diag(S)@Vt)

# ex1.1
def compression_rang_k(A,k):
    U,S,Vt = np.linalg.svd(A,full_matrices = False)
    return U[:,:k] @ np.diag(S[:k]) @ Vt[:k,:]

def compress_rgb(img,k):
    result = np.zeros_like(img,dtype=float)
    for c in range(3):
        result[:,:,c] = compression_rang_k(img[:,:,c], k)
    return np.clip(result, 0, 255).astype(np.uint8)
# plt.imshow(compress_rgb(img_rgb, 10))
# plt.show()

def pooling_compress(img,kernel_size=4,mode="avg"):
    '''single channel pooling'''
    h, w = img.shape
    kh, kw = kernel_size, kernel_size

    out_h, out_w = h // kh, w // kw
    out = np.zeros((out_h,out_w))

    for i in range(out_h):
        for j in range(out_w):
            patch = img[i*kh:(i+1)*kh, j*kw:(j+1)*kw]
            out[i,j] = patch.mean() if mode == "avg" else patch.max() 
    return out

def unpooling(img,kernel_size):
    '''single channel unpooling'''
    return np.repeat(np.repeat(img, kernel_size, axis=0), kernel_size, axis=1)


def mean_pool_rgb(img,ks=8,mode='avg'):
    h, w = img.shape[:2]
    pooled_rgb = np.zeros_like(img, dtype=float)
    for c in range(3):
        compressed = pooling_compress(img[:,:,c].astype(float), ks, mode=mode)
        up = unpooling(compressed,ks)
        pooled_rgb[:, :, c] = cv2.resize(up, (w, h), interpolation=cv2.INTER_NEAREST)
    
    pooled_rgb = np.clip(pooled_rgb,0,255).astype(np.uint8)
    return pooled_rgb

# plt.imshow(mean_pool_rgb(img_rgb, ks=4))
# plt.show()


fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 原图
axes[0].imshow(img_rgb)
axes[0].set_title("origin")
axes[0].axis("off")

# SVD 压缩
axes[1].imshow(compress_rgb(img_rgb, k=20))
axes[1].set_title("SVD (k=20)")
axes[1].axis("off")

# 池化压缩
axes[2].imshow(mean_pool_rgb(img_rgb, ks=50))
axes[2].set_title("mean pooling (ks=10)")
axes[2].axis("off")

plt.tight_layout()
plt.show()
