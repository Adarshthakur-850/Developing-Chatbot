import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import pickle
import os

class IntentClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        # Basic training data to start with
        self.X_train = [
            "hello", "hi", "hey there", "good morning",
            "bye", "goodbye", "see you later", "exit",
            "what can you do?", "help", "capabilities",
            "what is your name?", "who are you?",
            "tell me about python", "python info",
            "thank you", "thanks"
        ]
        self.y_train = [
            "greeting", "greeting", "greeting", "greeting",
            "farewell", "farewell", "farewell", "farewell",
            "help", "help", "help",
            "identity", "identity",
            "knowledge", "knowledge",
            "thanks", "thanks"
        ]
        self._train()

    def _train(self):
        """Trains the intent classifier."""
        self.model = make_pipeline(TfidfVectorizer(), SVC(probability=True))
        self.model.fit(self.X_train, self.y_train)
        print("Intent Classifier trained.")

    def predict(self, text):
        """Returns the predicted intent and confidence."""
        if not self.model:
            self._train()
            
        probas = self.model.predict_proba([text])[0]
        max_idx = np.argmax(probas)
        confidence = probas[max_idx]
        label = self.model.classes_[max_idx]
        
        return label, confidence
