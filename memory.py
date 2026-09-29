import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class IncidentMemory:

    def __init__(self, file_path="seed_incidents.json"):

        self.file_path = file_path

        with open(file_path, "r") as file:
            self.incidents = json.load(file)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.refresh_embeddings()

    def refresh_embeddings(self):

        texts = []

        for incident in self.incidents:

            text = (
                incident["system"] + " "
                + incident["error"] + " "
                + incident["root_cause"]
            )

            texts.append(text)

        self.embeddings = self.model.encode(texts)

    def search(self, query):

        query_embedding = self.model.encode([query])

        scores = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        best_index = scores.argmax()

        best_incident = self.incidents[best_index]

        similarity = float(scores[best_index])

        return best_incident, similarity

    def save_incident(
        self,
        system,
        error,
        root_cause,
        resolution
    ):

        new_incident = {
            "id": f"INC-{len(self.incidents)+1:03}",
            "system": system,
            "error": error,
            "root_cause": root_cause,
            "resolution": resolution
        }

        self.incidents.append(new_incident)

        with open(self.file_path, "w") as file:
            json.dump(
                self.incidents,
                file,
                indent=4
            )

        self.refresh_embeddings()

        return new_incident