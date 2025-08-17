"""
Unit tests for participant extraction service.
"""

import pytest
from src.services.participant_extraction import ParticipantExtractor, ParticipantInfo


class TestParticipantExtractor:
    """Test cases for ParticipantExtractor service."""

    def test_extract_basic_speaker_format(self):
        """Test extraction with basic 'Name:' format."""
        
        transcript = """
        John Doe: Welcome to today's session.
        Jane Smith: Thank you for having me.
        John Doe: How are you feeling today?
        Jane Smith: I'm doing well, thanks for asking.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 2
        names = [p.name for p in participants]
        assert "John Doe" in names
        assert "Jane Smith" in names

    def test_extract_bracketed_speaker_format(self):
        """Test extraction with '[Name]:' format."""
        
        transcript = """
        [Coach Sarah]: How did the week go for you?
        [Client Mike]: It was challenging but productive.
        [Coach Sarah]: Can you tell me more about the challenges?
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 2
        names = [p.name for p in participants]
        assert "Coach Sarah" in names
        assert "Client Mike" in names

    def test_extract_role_prefix_format(self):
        """Test extraction with 'Coach Name:' and 'Client Name:' format."""
        
        transcript = """
        Coach Jennifer: Let's start with your goals for this session.
        Client Robert: I want to work on my communication skills.
        Coach Jennifer: That's a great focus area.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 2
        names = [p.name for p in participants]
        assert "Jennifer" in names
        assert "Robert" in names

    def test_extract_role_suffix_format(self):
        """Test extraction with 'Name (Role):' format."""
        
        transcript = """
        Mary Johnson (Coach): How are you progressing with your action items?
        David Wilson (Client): I've completed most of them successfully.
        Mary Johnson (Coach): That's excellent progress.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 2
        names = [p.name for p in participants]
        assert "Mary Johnson" in names
        assert "David Wilson" in names

    def test_role_assignment_coach_indicators(self):
        """Test that coach role is correctly assigned based on context."""
        
        transcript = """
        Coach Lisa: Welcome to our coaching session today.
        Tom: Thank you, I'm excited to be here.
        Coach Lisa: Let's discuss your goals.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        coach_participant = next((p for p in participants if p.name == "Lisa"), None)
        client_participant = next((p for p in participants if p.name == "Tom"), None)
        
        assert coach_participant is not None
        assert coach_participant.role == "coach"
        
        assert client_participant is not None
        assert client_participant.role == "participant"

    def test_filter_invalid_names(self):
        """Test that invalid or generic names are filtered out."""
        
        transcript = """
        Speaker: This should be filtered out.
        Unknown: This too.
        User: And this.
        John Smith: This is a valid name.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 1
        assert participants[0].name == "John Smith"

    def test_deduplication_exact_names(self):
        """Test that exact duplicate names are deduplicated."""
        
        transcript = """
        Alice Cooper: First message.
        Bob Jones: Response.
        Alice Cooper: Second message.
        Bob Jones: Another response.
        Alice Cooper: Third message.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 2
        names = [p.name for p in participants]
        assert "Alice Cooper" in names
        assert "Bob Jones" in names

    def test_deduplication_similar_names(self):
        """Test that similar names are deduplicated."""
        
        transcript = """
        Dr. Sarah Wilson: First message.
        Sarah Wilson: Second message.
        Ms. Sarah Wilson: Third message.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        # Should be deduplicated to one participant
        assert len(participants) == 1
        assert "Sarah Wilson" in participants[0].name

    def test_name_validation_edge_cases(self):
        """Test name validation with edge cases."""
        
        # Test minimum length
        assert not ParticipantExtractor._is_valid_name("A")
        assert not ParticipantExtractor._is_valid_name("")
        
        # Test maximum length
        long_name = "A" * 51
        assert not ParticipantExtractor._is_valid_name(long_name)
        
        # Test special characters
        assert not ParticipantExtractor._is_valid_name("123456")
        assert not ParticipantExtractor._is_valid_name("@#$%")
        
        # Test valid names
        assert ParticipantExtractor._is_valid_name("John Doe")
        assert ParticipantExtractor._is_valid_name("Mary-Jane Smith")
        assert ParticipantExtractor._is_valid_name("O'Connor")
        assert ParticipantExtractor._is_valid_name("Dr. Johnson")

    def test_normalize_name_functionality(self):
        """Test name normalization for deduplication."""
        
        # Test basic normalization
        assert ParticipantExtractor._normalize_name("John Doe") == "john doe"
        assert ParticipantExtractor._normalize_name("  JANE   SMITH  ") == "jane smith"
        
        # Test title removal
        assert ParticipantExtractor._normalize_name("Dr. Sarah Wilson") == "sarah wilson"
        assert ParticipantExtractor._normalize_name("Mr. Bob Jones") == "bob jones"
        assert ParticipantExtractor._normalize_name("Mrs. Alice Cooper") == "alice cooper"

    def test_complex_transcript_realistic_scenario(self):
        """Test with a realistic, complex transcript."""
        
        transcript = """
        Coach Jennifer Martinez: Good morning, Sarah. How are you feeling today?
        
        Sarah Thompson: I'm doing well, thank you. I've been thinking about our last session.
        
        Coach Jennifer Martinez: That's great to hear. What specifically has been on your mind?
        
        Sarah Thompson: The goal-setting exercise we did. I realized I need to be more specific with my objectives.
        
        Coach Jennifer Martinez: Excellent insight. Can you share one goal you'd like to refine?
        
        Sarah Thompson: I want to improve my public speaking, but I think I need to break it down more.
        
        Coach Jennifer Martinez: Perfect. Let's work on making that more actionable.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        assert len(participants) == 2
        
        names = [p.name for p in participants]
        assert "Jennifer Martinez" in names
        assert "Sarah Thompson" in names
        
        # Check role assignment
        coach = next((p for p in participants if "Jennifer" in p.name), None)
        client = next((p for p in participants if "Sarah" in p.name), None)
        
        assert coach is not None
        assert coach.role == "coach"
        
        assert client is not None
        assert client.role == "participant"

    def test_mixed_format_transcript(self):
        """Test transcript with mixed speaker formats."""
        
        transcript = """
        [Facilitator Alex]: Welcome everyone to today's group session.
        
        Participant 1 (Maya): Thank you for organizing this.
        
        Client Ben: I'm excited to be here.
        
        Coach Alex: Let's start with introductions.
        
        Maya Rodriguez: I'll go first. I'm working on time management.
        
        Ben Carter: I'm focusing on leadership skills.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        # Should extract Alex, Maya, and Ben (filtering out generic "Participant 1")
        names = [p.name for p in participants]
        
        assert "Alex" in names
        assert "Maya Rodriguez" in names or "Maya" in names
        assert "Ben Carter" in names or "Ben" in names

    def test_extract_simple_names_method(self):
        """Test the simple name extraction method."""
        
        transcript = """
        Coach Lisa: How was your week?
        Michael: It was productive, thank you.
        Coach Lisa: Tell me more about that.
        """
        
        names = ParticipantExtractor.extract_simple_names(transcript)
        
        assert len(names) == 2
        assert "Lisa" in names
        assert "Michael" in names

    def test_empty_transcript(self):
        """Test behavior with empty transcript."""
        
        participants = ParticipantExtractor.extract_participants("")
        assert len(participants) == 0
        
        participants = ParticipantExtractor.extract_participants("   ")
        assert len(participants) == 0

    def test_transcript_without_speakers(self):
        """Test transcript without clear speaker indicators."""
        
        transcript = """
        This is just a regular text without any speaker indicators.
        It contains some names like John and Mary, but they're not formatted as speakers.
        The text continues without any clear structure.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        assert len(participants) == 0

    def test_confidence_scoring(self):
        """Test confidence scoring for role assignment."""
        
        transcript = """
        Therapist Dr. Wilson: How are you coping with the changes?
        Client Sarah: It's been challenging but I'm managing.
        Dr. Wilson: That shows great resilience.
        """
        
        participants = ParticipantExtractor.extract_participants(transcript)
        
        coach = next((p for p in participants if "Wilson" in p.name), None)
        assert coach is not None
        assert coach.role == "coach"
        assert coach.confidence > 0.7  # Should have high confidence due to "Therapist" indicator

    def test_select_best_participant_logic(self):
        """Test the logic for selecting the best participant from similar names."""
        
        # Create test participant group
        participants = [
            ParticipantInfo("John", confidence=0.8),
            ParticipantInfo("John Doe", confidence=0.8),
            ParticipantInfo("J. Doe", confidence=0.6),
        ]
        
        best = ParticipantExtractor._select_best_participant(participants)
        
        # Should prefer longer, more complete name when confidence is equal
        assert best.name == "John Doe"