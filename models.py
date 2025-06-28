from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class User:
    """User model for the platform"""
    id: int
    username: str
    email: str
    password_hash: str
    user_type: str  # 'founder', 'investor', 'partner', 'service_provider'
    full_name: str
    bio: str
    location: str
    industry: str
    experience: str
    created_at: datetime
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create_password_hash(password: str) -> str:
        """Create password hash"""
        return generate_password_hash(password)

@dataclass
class Startup:
    """Startup model"""
    id: int
    founder_id: int
    name: str
    description: str
    industry: str
    stage: str  # 'idea', 'prototype', 'mvp', 'scaling', 'established'
    funding_needed: str
    location: str
    website: str
    pitch_deck: str
    team_size: int
    revenue: str
    looking_for: List[str]  # ['investors', 'partners', 'service_providers']
    created_at: datetime

@dataclass
class Connection:
    """Connection/Message model"""
    id: int
    sender_id: int
    receiver_id: int
    startup_id: Optional[int]
    message: str
    status: str  # 'pending', 'accepted', 'declined'
    created_at: datetime

@dataclass
class Message:
    """Direct message model"""
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    read: bool
