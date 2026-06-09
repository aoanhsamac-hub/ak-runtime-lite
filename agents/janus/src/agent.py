class JanusAgent:
    id = "janus"

    def status(self):
        return {"agent": self.id, "status": "bootstrap"}
