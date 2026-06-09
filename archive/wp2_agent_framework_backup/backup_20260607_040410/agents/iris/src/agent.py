class IrisAgent:
    id = "iris"

    def status(self):
        return {"agent": self.id, "status": "bootstrap"}
