"""Loads the trained model and runs inference."""

import torch
from services.orchestra_transformer import OrchestraTransformer
from services.model_input_builder import build_model_inputs
from services.model_output_parser import parse_model_output
from models.arrangement_request import ArrangementRequest
from config import Config


class ModelRunner:
    """Singleton that loads the model once and runs inference."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def _load(self):
        if self._loaded:
            return
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = OrchestraTransformer().to(self.device)
        state_dict = torch.load(Config.MODEL_PATH, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        self._loaded = True

    def run(
        self,
        melody_midi_path: str,
        harmony_midi_path: str,
        request: ArrangementRequest,
        bpm: float,
        output_midi_path: str
    ) -> str:
        """
        Run inference: MIDI files + preferences → generated arrangement MIDI.

        Returns:
            path to the generated MIDI file
        """
        self._load()

        inputs = build_model_inputs(melody_midi_path, harmony_midi_path, request, self.device)

        with torch.inference_mode():
            logits = self.model(
                inputs["melody_in"],
                inputs["harmony_guide"],
                inputs["global_cond"],
                inputs["inst_indices"]
            )

        predictions = torch.argmax(logits, dim=-1).squeeze(0).cpu().numpy()

        return parse_model_output(predictions, request, bpm, output_midi_path)
