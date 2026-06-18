from app.schemas.profile import UserProfile, ProfileDelta

class SessionManager:
    """
    In-memory storage for conversational profile memory.
    Maps session_id -> UserProfile.
    """
    def __init__(self):
        self._sessions: dict[str, UserProfile] = {}

    def get_profile(self, session_id: str) -> UserProfile:
        if session_id not in self._sessions:
            self._sessions[session_id] = UserProfile()
        return self._sessions[session_id]

    def update_profile(self, session_id: str, delta: ProfileDelta) -> UserProfile:
        profile = self.get_profile(session_id)
        profile.merge_delta(delta)
        return profile

    def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]
