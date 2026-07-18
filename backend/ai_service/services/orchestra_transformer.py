"""OrchestraTransformer architecture - must match training code exactly."""

import math
import torch
import torch.nn as nn

# ── קבועי ארכיטקטורה ──────────────────────────────────────────────────────────
SEQ_LEN           = 256   # אורך רצף התווים (16th notes)
MAX_TRACKS        = 8     # מספר מקסימלי של כלים במקביל
NUM_MIDI_PROGRAMS = 128   # מספר תוכניות MIDI סטנדרטיות (0-127)
NUM_NOTES         = 128   # ערכי pitch אפשריים (0-127)
NUM_CLASSES       = NUM_NOTES + 1  # 129: 128 תווים + token ריפוד (index 128)
PAD_TOKEN         = -1    # ערך ריפוד לפני המרה ל-tensor

# ── היפר-פרמטרים של ה-Transformer ─────────────────────────────────────────────
D_MODEL  = 256   # מימד ה-embedding
N_HEADS  = 8     # מספר ראשי attention (D_MODEL / N_HEADS = 32 לכל ראש)
N_LAYERS = 6     # מספר שכבות Transformer
D_FF     = 1024  # מימד שכבת ה-feedforward הפנימית
DROPOUT  = 0.15  # הסתברות Dropout למניעת overfitting


class PositionalEncoding(nn.Module):
    """
    מוסיף מידע על מיקום כל תו ברצף.
    ה-Transformer עצמו לא מודע לסדר — ה-PE מספק את המידע הזה.
    משתמש בפונקציות sin/cos בתדרים שונים לכל מימד.
    """
    def __init__(self, d_model, max_len=SEQ_LEN):
        super().__init__()
        pe       = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)

        # div_term — גורם חלוקה שיוצר תדרים שונים לכל זוג מימדים
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)  # מימדים זוגיים
        pe[:, 1::2] = torch.cos(position * div_term)  # מימדים אי-זוגיים

        # register_buffer — שומר את ה-PE כחלק מהמודל אבל לא כפרמטר לאימון
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        # הוספת ה-PE ל-embedding — [:, :x.size(1)] מתאים לאורך הרצף הנוכחי
        return x + self.pe[:, :x.size(1)]


class OrchestraTransformer(nn.Module):
    """
    מודל Transformer שמקבל מנגינה + הרמוניה + העדפות משתמש
    ומייצר arrangement מוזיקלי מלא עבור עד 8 כלים.
    """
    def __init__(self, d_model=D_MODEL, n_heads=N_HEADS, n_layers=N_LAYERS,
                 d_ff=D_FF, dropout=DROPOUT):
        super().__init__()

        # Embeddings — ממירים אינדקסים למרחב וקטורי רציף
        self.melody_embed     = nn.Embedding(NUM_CLASSES, d_model, padding_idx=NUM_CLASSES - 1)
        self.harmony_embed    = nn.Embedding(NUM_CLASSES, d_model, padding_idx=NUM_CLASSES - 1)
        self.instrument_embed = nn.Embedding(NUM_MIDI_PROGRAMS + 1, d_model, padding_idx=NUM_MIDI_PROGRAMS)

        self.pos_encoder  = PositionalEncoding(d_model)

        # שכבה ליניארית שממירה את וקטור ה-conditioning (10 ערכים) למרחב ה-embedding
        self.cond_linear  = nn.Linear(10, d_model)

        # ליבת ה-Transformer — N_LAYERS שכבות של self-attention + feedforward
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=d_ff,
            dropout=dropout, batch_first=True  # batch_first=True: [B, seq, features]
        )
        self.transformer_blocks = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)

        # שכבת פלט — ממירה כל step ל-8*129 logits (8 כלים × 129 classes)
        self.output_layer = nn.Linear(d_model, MAX_TRACKS * NUM_CLASSES)
        self.dropout      = nn.Dropout(dropout)

    def forward(self, melody_input, harmony_guide, global_conditions, input_instruments):
        device     = melody_input.device
        batch_size = melody_input.size(0)

        # החלפת PAD_TOKEN (-1) בערך ה-padding_idx של ה-embedding
        melody_input      = torch.where(melody_input      == PAD_TOKEN, torch.tensor(NUM_CLASSES - 1,   device=device), melody_input)
        harmony_guide     = torch.where(harmony_guide     == PAD_TOKEN, torch.tensor(NUM_CLASSES - 1,   device=device), harmony_guide)
        input_instruments = torch.where(input_instruments == PAD_TOKEN, torch.tensor(NUM_MIDI_PROGRAMS, device=device), input_instruments)

        # Embedding + Positional Encoding למנגינה ולהרמוניה
        m_emb    = self.pos_encoder(self.melody_embed(melody_input))    # [B, 256, 256]
        h_emb    = self.pos_encoder(self.harmony_embed(harmony_guide))  # [B, 256, 256]
        combined = m_emb + h_emb  # חיבור מנגינה + הרמוניה

        # Embedding לכלים — ממוצע על כל הכלים, מורחב לכל ה-steps
        inst_emb = self.instrument_embed(input_instruments).mean(dim=1, keepdim=True).expand(-1, SEQ_LEN, -1)

        # Conditioning vector — סגנון, קושי, קולות, כלים
        cond_emb = self.cond_linear(global_conditions).unsqueeze(1).expand(-1, SEQ_LEN, -1)

        # חיבור כל המרכיבים + Dropout לפני ה-Transformer
        x = self.dropout(combined + inst_emb + cond_emb)

        # הרצת ה-Transformer blocks
        transformer_out = self.transformer_blocks(x)  # [B, 256, 256]

        # שכבת פלט → reshape ל-[B, 8, 256, 129]
        logits = self.output_layer(transformer_out)                         # [B, 256, 8*129]
        logits = logits.view(batch_size, SEQ_LEN, MAX_TRACKS, NUM_CLASSES)  # [B, 256, 8, 129]
        logits = logits.permute(0, 2, 1, 3)                                 # [B, 8, 256, 129]
        return logits.contiguous()
