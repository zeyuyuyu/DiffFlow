import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class DiffFlow(nn.Module):
    def __init__(self, input_dim, hidden_dims=[64, 128, 64], dropout=0.1, clip_threshold=1.0):
        super().__init__()
        self.input_dim = input_dim
        self.clip_threshold = clip_threshold
        
        # Build network layers
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
            
        self.network = nn.Sequential(*layers)
        self.output_layer = nn.Linear(prev_dim, input_dim)
        
    def forward(self, x, time):
        # Time embedding
        time_emb = self._get_time_embedding(time)
        x = torch.cat([x, time_emb], dim=-1)
        
        # Apply network with gradient clipping
        with torch.enable_grad():
            x.requires_grad_(True)
            hidden = self.network(x)
            output = self.output_layer(hidden)
            
            # Adaptive gradient clipping
            if self.training:
                gradients = torch.autograd.grad(output.sum(), x, create_graph=True)[0]
                grad_norm = gradients.norm(p=2, dim=-1)
                
                # Calculate clipping factor
                clip_coef = (self.clip_threshold / (grad_norm + 1e-6)).clamp(max=1.0)
                output = output * clip_coef.unsqueeze(-1)
        
        return output
    
    def _get_time_embedding(self, time):
        # Sinusoidal time embedding
        freqs = torch.exp(
            -math.log(10000) * torch.arange(start=0, end=self.input_dim//4) / (self.input_dim//4)
        ).to(time.device)
        
        args = time[:, None] * freqs[None]
        embedding = torch.cat([torch.cos(args), torch.sin(args)], dim=-1)
        if self.input_dim % 2:
            embedding = torch.cat([embedding, torch.zeros_like(embedding[:, :1])], dim=-1)
        
        return embedding
    
    def loss_fn(self, x0, t, noise):
        x_noisy = x0 + noise * torch.sqrt(t.reshape(-1, 1))
        predicted = self(x_noisy, t)
        return F.mse_loss(predicted, noise)
