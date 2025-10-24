"""
AI-related Pydantic schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class AIAnalysisResponse(BaseModel):
    """AI analysis response schema"""
    analysis_type: str
    result: Dict[str, Any]
    confidence: float
    processing_time: float
    timestamp: datetime = datetime.now()

class VisionAnalysisRequest(BaseModel):
    """Vision analysis request schema"""
    image_url: Optional[str] = None
    analysis_type: str = "property_condition"
    confidence_threshold: float = 0.7

class NLPProcessingRequest(BaseModel):
    """NLP processing request schema"""
    text: str
    analysis_type: str = "sentiment"
    language: str = "en"

class VoiceAnalysisRequest(BaseModel):
    """Voice analysis request schema"""
    audio_url: Optional[str] = None
    analysis_type: str = "sentiment"
    language: str = "en"

class AIMetrics(BaseModel):
    """AI metrics schema"""
    total_analyses: int
    success_rate: float
    average_confidence: float
    processing_time_avg: float
    last_updated: datetime

class VisionMetrics(AIMetrics):
    """Vision analysis metrics schema"""
    total_images_processed: int
    accuracy_rate: float
    analysis_types: Dict[str, int]

class NLPMetrics(AIMetrics):
    """NLP processing metrics schema"""
    total_text_processed: int
    language_distribution: Dict[str, int]
    sentiment_distribution: Dict[str, int]

class VoiceMetrics(AIMetrics):
    """Voice AI metrics schema"""
    total_calls_processed: int
    average_call_duration: float
    sentiment_distribution: Dict[str, int]

class BlockchainMetrics(AIMetrics):
    """Blockchain transaction metrics schema"""
    total_transactions: int
    success_rate: float
    average_transaction_time: float
    gas_usage_avg: float
