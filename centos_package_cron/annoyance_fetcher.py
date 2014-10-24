from annoyance_check import AnnoyanceCheck

class AnnoyanceFetcher:    
    def fetch(self, session):
        return AnnoyanceCheck(session)
        