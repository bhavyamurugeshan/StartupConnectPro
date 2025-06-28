from typing import Dict, List, Optional
from models import User, Startup, Connection, Message
from datetime import datetime

class DataStore:
    """In-memory data store for the application"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.startups: Dict[int, Startup] = {}
        self.connections: List[Connection] = []
        self.messages: List[Message] = []
        self._user_counter = 1
        self._startup_counter = 1
        self._connection_counter = 1
        self._message_counter = 1
    
    # User methods
    def create_user(self, username: str, email: str, password: str, user_type: str, 
                   full_name: str, bio: str = "", location: str = "", 
                   industry: str = "", experience: str = "") -> User:
        """Create a new user"""
        user = User(
            id=self._user_counter,
            username=username,
            email=email,
            password_hash=User.create_password_hash(password),
            user_type=user_type,
            full_name=full_name,
            bio=bio,
            location=location,
            industry=industry,
            experience=experience,
            created_at=datetime.now()
        )
        self.users[self._user_counter] = user
        self._user_counter += 1
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    # Startup methods
    def create_startup(self, founder_id: int, name: str, description: str, 
                      industry: str, stage: str, funding_needed: str, 
                      location: str, website: str = "", pitch_deck: str = "",
                      team_size: int = 1, revenue: str = "", 
                      looking_for: List[str] = None) -> Startup:
        """Create a new startup"""
        if looking_for is None:
            looking_for = []
        
        startup = Startup(
            id=self._startup_counter,
            founder_id=founder_id,
            name=name,
            description=description,
            industry=industry,
            stage=stage,
            funding_needed=funding_needed,
            location=location,
            website=website,
            pitch_deck=pitch_deck,
            team_size=team_size,
            revenue=revenue,
            looking_for=looking_for,
            created_at=datetime.now()
        )
        self.startups[self._startup_counter] = startup
        self._startup_counter += 1
        return startup
    
    def get_startup_by_id(self, startup_id: int) -> Optional[Startup]:
        """Get startup by ID"""
        return self.startups.get(startup_id)
    
    def get_startups_by_founder(self, founder_id: int) -> List[Startup]:
        """Get all startups by founder"""
        return [startup for startup in self.startups.values() 
                if startup.founder_id == founder_id]
    
    def search_startups(self, query: str = "", industry: str = "", 
                       stage: str = "", looking_for: str = "") -> List[Startup]:
        """Search startups with filters"""
        results = list(self.startups.values())
        
        if query:
            query_lower = query.lower()
            results = [s for s in results if 
                      query_lower in s.name.lower() or 
                      query_lower in s.description.lower()]
        
        if industry:
            results = [s for s in results if s.industry == industry]
        
        if stage:
            results = [s for s in results if s.stage == stage]
        
        if looking_for:
            results = [s for s in results if looking_for in s.looking_for]
        
        return results
    
    # Connection methods
    def create_connection(self, sender_id: int, receiver_id: int, 
                         startup_id: Optional[int], message: str) -> Connection:
        """Create a new connection request"""
        connection = Connection(
            id=self._connection_counter,
            sender_id=sender_id,
            receiver_id=receiver_id,
            startup_id=startup_id,
            message=message,
            status='pending',
            created_at=datetime.now()
        )
        self.connections.append(connection)
        self._connection_counter += 1
        return connection
    
    def get_connections_for_user(self, user_id: int) -> List[Connection]:
        """Get all connections for a user (sent and received)"""
        return [conn for conn in self.connections 
                if conn.sender_id == user_id or conn.receiver_id == user_id]
    
    def update_connection_status(self, connection_id: int, status: str) -> bool:
        """Update connection status"""
        for conn in self.connections:
            if conn.id == connection_id:
                conn.status = status
                return True
        return False
    
    # Message methods
    def create_message(self, sender_id: int, receiver_id: int, content: str) -> Message:
        """Create a new message"""
        message = Message(
            id=self._message_counter,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            created_at=datetime.now(),
            read=False
        )
        self.messages.append(message)
        self._message_counter += 1
        return message
    
    def get_messages_between_users(self, user1_id: int, user2_id: int) -> List[Message]:
        """Get all messages between two users"""
        return [msg for msg in self.messages 
                if (msg.sender_id == user1_id and msg.receiver_id == user2_id) or
                   (msg.sender_id == user2_id and msg.receiver_id == user1_id)]
    
    def get_conversations_for_user(self, user_id: int) -> List[int]:
        """Get list of user IDs that have conversations with given user"""
        conversations = set()
        for msg in self.messages:
            if msg.sender_id == user_id:
                conversations.add(msg.receiver_id)
            elif msg.receiver_id == user_id:
                conversations.add(msg.sender_id)
        return list(conversations)

# Global data store instance
data_store = DataStore()
