from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


class Predictor:
    """
    ModernBERT inference class.

    Returns:
        - Prediction
        - AI Probability
        - Human Probability
        - Confidence
    """

    def __init__(self, model_path="model"):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path
        )

        self.model.to(self.device)
        self.model.eval()

    # -------------------------------------------------------
    # Predict one text
    # -------------------------------------------------------

    @torch.no_grad()
    def predict(self, text):

        inputs = self.tokenizer(
            text,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )

        inputs = {
            k: v.to(self.device)
            for k, v in inputs.items()
        }

        outputs = self.model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )[0]

        human_probability = probabilities[0].item()
        ai_probability = probabilities[1].item()

        if ai_probability >= human_probability:

            label = "AI"
            confidence = ai_probability

        else:

            label = "Human"
            confidence = human_probability

        return {

            "label": label,

            "confidence": round(confidence, 4),

            "human_probability": round(
                human_probability,
                4
            ),

            "ai_probability": round(
                ai_probability,
                4
            ),
        }

    # -------------------------------------------------------
    # Batch prediction
    # -------------------------------------------------------

    @torch.no_grad()
    def predict_batch(
        self,
        texts,
        batch_size=32
    ):

        results = []

        for start in range(
            0,
            len(texts),
            batch_size,
        ):

            batch = texts[
                start:start + batch_size
            ]

            inputs = self.tokenizer(
                batch,
                truncation=True,
                max_length=512,
                padding=True,
                return_tensors="pt",
            )

            inputs = {
                k: v.to(self.device)
                for k, v in inputs.items()
            }

            outputs = self.model(**inputs)

            probabilities = torch.softmax(
                outputs.logits,
                dim=1
            )

            for probs in probabilities:

                human_probability = probs[0].item()
                ai_probability = probs[1].item()

                if ai_probability >= human_probability:

                    label = "AI"
                    confidence = ai_probability

                else:

                    label = "Human"
                    confidence = human_probability

                results.append({

                    "label": label,

                    "confidence": round(
                        confidence,
                        4
                    ),

                    "human_probability": round(
                        human_probability,
                        4
                    ),

                    "ai_probability": round(
                        ai_probability,
                        4
                    ),
                })

        return results