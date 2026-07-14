"""OrchestraTransformer architecture - must match training code exactly."""

import math
import torch
import torch.nn as nn

SEQ_LEN = 256
MAX_TRACKS = 8
NUM_MIDI_PROGRAMS = 128
NUM_NOTES = 128
NUM_CLASSES = NUM_NOTES + 1  # 129 (index 128 = PAD)
PAD_TOKEN = -1

D_MODEL = 256
N_HEADS = 8
N_LAYERS = 6
D_FF = 1024
DROPOUT = 0.15


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=SEQ_LEN):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]


class OrchestraTransformer(nn.Module):
    def __init__(self, d_model=D_MODEL, n_heads=N_HEADS, n_layers=N_LAYERS, d_ff=D_FF, dropout=DROPOUT):
        super().__init__()
        self.melody_embed = nn.Embedding(NUM_CLASSES, d_model, padding_idx=NUM_CLASSES - 1)
        self.harmony_embed = nn.Embedding(NUM_CLASSES, d_model, padding_idx=NUM_CLASSES - 1)
        self.instrument_embed = nn.Embedding(NUM_MIDI_PROGRAMS + 1, d_model, padding_idx=NUM_MIDI_PROGRAMS)
        self.pos_encoder = PositionalEncoding(d_model)
        self.cond_linear = nn.Linear(10, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=d_ff,
            dropout=dropout, batch_first=True
        )
        self.transformer_blocks = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.output_layer = nn.Linear(d_model, MAX_TRACKS * NUM_CLASSES)
        self.dropout = nn.Dropout(dropout)

    def forward(self, melody_input, harmony_guide, global_conditions, input_instruments):
        device = melody_input.device
        batch_size = melody_input.size(0)

        melody_input      = torch.where(melody_input      == PAD_TOKEN, torch.tensor(NUM_CLASSES - 1,    device=device), melody_input)
        harmony_guide     = torch.where(harmony_guide     == PAD_TOKEN, torch.tensor(NUM_CLASSES - 1,    device=device), harmony_guide)
        input_instruments = torch.where(input_instruments == PAD_TOKEN, torch.tensor(NUM_MIDI_PROGRAMS,  device=device), input_instruments)

        m_emb = self.pos_encoder(self.melody_embed(melody_input))
        h_emb = self.pos_encoder(self.harmony_embed(harmony_guide))
        combined = m_emb + h_emb

        inst_emb = self.instrument_embed(input_instruments).mean(dim=1, keepdim=True).expand(-1, SEQ_LEN, -1)
        cond_emb = self.cond_linear(global_conditions).unsqueeze(1).expand(-1, SEQ_LEN, -1)

        x = self.dropout(combined + inst_emb + cond_emb)
        transformer_out = self.transformer_blocks(x)

        logits = self.output_layer(transformer_out)                        # [B, 256, 8*129]
        logits = logits.view(batch_size, SEQ_LEN, MAX_TRACKS, NUM_CLASSES) # [B, 256, 8, 129]
        logits = logits.permute(0, 2, 1, 3)                                # [B, 8, 256, 129]
        return logits.contiguous()
