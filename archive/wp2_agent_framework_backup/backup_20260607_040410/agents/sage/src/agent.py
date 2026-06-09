class SageAgent:
    id = "sage"

    def status(self):
        return {"agent": self.id, "status": "bootstrap"}
