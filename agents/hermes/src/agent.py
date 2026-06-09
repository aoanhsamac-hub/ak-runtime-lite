class HermesAgent:
    id = "hermes"

    def status(self):
        return {"agent": self.id, "status": "bootstrap"}
