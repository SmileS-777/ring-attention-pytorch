import torch

from ring_attention_pytorch import (
    default_attention,
    ring_flash_attn
)

# variables

causal = True
seq_len = 62
bucket_size = 4

# base qkv

q = torch.randn(2, seq_len, 2, 16)
k = torch.randn(2, seq_len, 2, 16)
v = torch.randn(2, seq_len, 2, 16)

# flash and regular qkv's

fq = q.clone().requires_grad_()
fk = k.clone().requires_grad_()
fv = v.clone().requires_grad_()

rq = q.clone().requires_grad_()
rk = k.clone().requires_grad_()
rv = v.clone().requires_grad_()

# forward

o = default_attention(rq, rk, rv, causal = causal)
fo = ring_flash_attn(fq, fk, fv, bucket_size = bucket_size, causal = causal)

assert torch.allclose(o, fo, atol = 1e-6)

# backwards

o.sum().backward()
fo.sum().backward()

assert torch.allclose(rq.grad, fq.grad, atol = 1e-6)
assert torch.allclose(rk.grad, fk.grad, atol = 1e-6)
assert torch.allclose(rv.grad, fv.grad, atol = 1e-6)

print('✅ outputs and gradients are same between regular attention and naive flash attention')
