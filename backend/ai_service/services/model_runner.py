"""Loads the trained model and runs inference."""

import torch
from services.orchestra_transformer import OrchestraTransformer
from services.model_input_builder import build_model_inputs
from services.model_output_parser import parse_model_output
from models.arrangement_request import ArrangementRequest
from config import Config


class ModelRunner:
    """
    Singleton שטוען את המודל פעם אחת בלבד לזיכרון.
    כל קריאה נוספת משתמשת באותו instance — חוסך זמן טעינה.
    """

    _instance = None

    def __new__(cls):
        # Singleton pattern — מחזיר את אותו instance בכל פעם
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def _load(self):
        """טוען את המודל מהדיסק לזיכרון — רק בפעם הראשונה."""
        if self._loaded:
            return  # כבר טעון — אין צורך לטעון שוב

        # בחירת device: GPU אם זמין, אחרת CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # יצירת ארכיטקטורת המודל ריקה
        self.model = OrchestraTransformer().to(self.device)

        # טעינת המשקלים המאומנים מהדיסק
        # weights_only=True — אבטחה: מונע הרצת קוד שרירותי בעת טעינה
        state_dict = torch.load(Config.MODEL_PATH, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)

        # מצב evaluation — מכבה Dropout ו-BatchNorm לאינפרנס
        self.model.eval()
        self._loaded = True

    def run(
        self,
        melody_midi_path:  str,
        harmony_midi_path: str,
        request:           ArrangementRequest,
        bpm:               float,
        output_midi_path:  str
    ) -> str:
        """
        Run inference: MIDI files + preferences → generated arrangement MIDI.

        Returns:
            path to the generated MIDI file
        """
        # טעינה עצלה (lazy loading) — טוען רק כשנדרש
        self._load()

        # בניית tensors מהקלט
        inputs = build_model_inputs(
            melody_midi_path, harmony_midi_path, request, self.device
        )

        # inference_mode — מהיר יותר מ-no_grad, מכבה מעקב גרדיאנטים לחלוטין
        with torch.inference_mode():
            logits = self.model(
                inputs["melody_in"],
                inputs["harmony_guide"],
                inputs["global_cond"],
                inputs["inst_indices"]
            )
            # logits shape: [1, 8, 256, 129] — batch=1, tracks=8, steps=256, classes=129

        # בחירת הנוטה עם ההסתברות הגבוהה ביותר לכל step
        # squeeze(0) מסיר את ה-batch dimension → shape: [8, 256]
        predictions = torch.argmax(logits, dim=-1).squeeze(0).cpu().numpy()

        # המרת ה-predictions ל-MIDI ושמירה לדיסק
        return parse_model_output(predictions, request, bpm, output_midi_path)
