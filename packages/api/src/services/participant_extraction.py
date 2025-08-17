"""
Participant extraction service for identifying names in transcripts.
"""

import re
from typing import List, Set, Dict, Any
from dataclasses import dataclass


@dataclass
class ParticipantInfo:
    """Information about an identified participant."""
    name: str
    role: str = "participant"  # "coach" or "participant"
    confidence: float = 1.0


class ParticipantExtractor:
    """Service for extracting participant names from transcripts."""
    
    # Common speaker patterns in transcripts
    SPEAKER_PATTERNS = [
        r'([A-Z][a-zA-Z\s]+):\s*',  # "John Doe: text"
        r'\[([A-Z][a-zA-Z\s]+)\]:\s*',  # "[John Doe]: text"
        r'Speaker\s+([A-Z][a-zA-Z\s]+):\s*',  # "Speaker John Doe: text"
        r'Coach\s+([A-Z][a-zA-Z\s]+):\s*',  # "Coach John: text"
        r'Client\s+([A-Z][a-zA-Z\s]+):\s*',  # "Client Jane: text"
        r'([A-Z][a-zA-Z\s]+)\s*\(Coach\):\s*',  # "John (Coach): text"
        r'([A-Z][a-zA-Z\s]+)\s*\(Client\):\s*',  # "Jane (Client): text"
    ]
    
    # Patterns to identify coach vs client
    COACH_INDICATORS = [
        r'coach',
        r'therapist',
        r'counselor',
        r'facilitator',
        r'supervisor',
    ]
    
    # Common names to filter out (system/generic terms)
    FILTER_NAMES = {
        'speaker', 'participant', 'user', 'client', 'coach', 'unknown',
        'person', 'individual', 'member', 'attendee', 'guest', 'host',
        'moderator', 'facilitator', 'interviewer', 'interviewee',
    }
    
    @classmethod
    def extract_participants(cls, transcript: str) -> List[ParticipantInfo]:
        """
        Extract participant names and roles from transcript text.
        
        Args:
            transcript: Raw transcript text
            
        Returns:
            List of ParticipantInfo objects with identified participants
        """
        participants = cls._find_speaker_names(transcript)
        participants = cls._assign_roles(participants, transcript)
        participants = cls._deduplicate_and_clean(participants)
        
        return participants
    
    @classmethod
    def _find_speaker_names(cls, transcript: str) -> List[ParticipantInfo]:
        """Find all potential speaker names using regex patterns."""
        found_names: Set[str] = set()
        
        for pattern in cls.SPEAKER_PATTERNS:
            matches = re.finditer(pattern, transcript, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip()
                if cls._is_valid_name(name):
                    found_names.add(name)
        
        return [ParticipantInfo(name=name) for name in found_names]
    
    @classmethod
    def _is_valid_name(cls, name: str) -> bool:
        """Validate if extracted text is likely a real name."""
        if not name or len(name) < 2:
            return False
        
        # Filter out generic terms
        if name.lower() in cls.FILTER_NAMES:
            return False
        
        # Must contain at least one letter
        if not re.search(r'[a-zA-Z]', name):
            return False
        
        # Reasonable length for a name
        if len(name) > 50:
            return False
        
        # Basic format validation - should look like a name
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            return False
        
        return True
    
    @classmethod
    def _assign_roles(cls, participants: List[ParticipantInfo], transcript: str) -> List[ParticipantInfo]:
        """Assign roles (coach vs participant) based on context."""
        transcript_lower = transcript.lower()
        
        for participant in participants:
            name_lower = participant.name.lower()
            
            # Look for coach indicators near the name
            coach_score = 0
            for indicator in cls.COACH_INDICATORS:
                # Check if coach indicators appear near this name
                pattern = rf'{re.escape(name_lower)}.{{0,50}}{indicator}|{indicator}.{{0,50}}{re.escape(name_lower)}'
                if re.search(pattern, transcript_lower):
                    coach_score += 1
            
            # If strong coach indicators, mark as coach
            if coach_score >= 1:
                participant.role = "coach"
            
            # Adjust confidence based on how clearly the role is indicated
            if coach_score > 0:
                participant.confidence = min(1.0, 0.7 + (coach_score * 0.15))
        
        return participants
    
    @classmethod
    def _deduplicate_and_clean(cls, participants: List[ParticipantInfo]) -> List[ParticipantInfo]:
        """Remove duplicates and clean up participant list."""
        # Group by normalized name to handle variations
        name_groups: Dict[str, List[ParticipantInfo]] = {}
        
        for participant in participants:
            normalized = cls._normalize_name(participant.name)
            if normalized not in name_groups:
                name_groups[normalized] = []
            name_groups[normalized].append(participant)
        
        # For each group, pick the best representative
        final_participants = []
        for normalized_name, group in name_groups.items():
            best_participant = cls._select_best_participant(group)
            final_participants.append(best_participant)
        
        return final_participants
    
    @classmethod
    def _normalize_name(cls, name: str) -> str:
        """Normalize name for deduplication."""
        # Convert to lowercase, remove extra spaces, standardize
        normalized = re.sub(r'\s+', ' ', name.lower().strip())
        
        # Remove common title variations
        normalized = re.sub(r'^(mr|mrs|ms|dr|prof)\.?\s*', '', normalized)
        
        return normalized
    
    @classmethod
    def _select_best_participant(cls, group: List[ParticipantInfo]) -> ParticipantInfo:
        """Select the best participant from a group of similar names."""
        # Prefer higher confidence
        group.sort(key=lambda p: p.confidence, reverse=True)
        
        best = group[0]
        
        # If multiple with same confidence, prefer more complete names
        same_confidence = [p for p in group if p.confidence == best.confidence]
        if len(same_confidence) > 1:
            # Prefer longer names (more complete)
            same_confidence.sort(key=lambda p: len(p.name), reverse=True)
            best = same_confidence[0]
        
        return best
    
    @classmethod
    def extract_simple_names(cls, transcript: str) -> List[str]:
        """Simple extraction returning just name strings."""
        participants = cls.extract_participants(transcript)
        return [p.name for p in participants]