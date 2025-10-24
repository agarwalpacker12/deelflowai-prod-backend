"""
AI services endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
from app.core.security import get_current_user, require_permission
from app.core.exceptions import NotFoundError, AuthorizationError
from app.services.ai_service import AIService
from app.schemas.ai import AIAnalysisResponse, VisionAnalysisRequest, NLPProcessingRequest
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/vision/analyze", response_model=AIAnalysisResponse)
async def analyze_property_image(
    file: UploadFile = File(...),
    analysis_type: str = "property_condition",
    current_user = Depends(get_current_user)
):
    """Analyze property image using AI vision"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "use_ai_vision"):
            raise AuthorizationError("Permission to use AI vision required")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read file content
        content = await file.read()
        
        # Perform analysis
        analysis = await ai_service.analyze_image(content, analysis_type)
        
        return AIAnalysisResponse(
            analysis_type="vision",
            result=analysis,
            confidence=analysis.get("confidence", 0.0),
            processing_time=analysis.get("processing_time", 0.0)
        )
    
    except Exception as e:
        logger.error(f"Vision analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze image"
        )

@router.post("/nlp/process", response_model=AIAnalysisResponse)
async def process_text(
    request: NLPProcessingRequest,
    current_user = Depends(get_current_user)
):
    """Process text using NLP"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "use_ai_nlp"):
            raise AuthorizationError("Permission to use AI NLP required")
        
        # Process text
        result = await ai_service.process_text(
            request.text,
            request.analysis_type,
            request.language
        )
        
        return AIAnalysisResponse(
            analysis_type="nlp",
            result=result,
            confidence=result.get("confidence", 0.0),
            processing_time=result.get("processing_time", 0.0)
        )
    
    except Exception as e:
        logger.error(f"NLP processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process text"
        )

@router.post("/voice/analyze")
async def analyze_voice_call(
    audio_file: UploadFile = File(...),
    analysis_type: str = "sentiment",
    current_user = Depends(get_current_user)
):
    """Analyze voice call using AI"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "use_ai_voice"):
            raise AuthorizationError("Permission to use AI voice required")
        
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an audio file"
            )
        
        # Read file content
        content = await audio_file.read()
        
        # Perform analysis
        analysis = await ai_service.analyze_audio(content, analysis_type)
        
        return AIAnalysisResponse(
            analysis_type="voice",
            result=analysis,
            confidence=analysis.get("confidence", 0.0),
            processing_time=analysis.get("processing_time", 0.0)
        )
    
    except Exception as e:
        logger.error(f"Voice analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze audio"
        )

@router.get("/metrics/overall")
async def get_overall_ai_metrics(
    current_user = Depends(get_current_user)
):
    """Get overall AI performance metrics"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "view_ai_metrics"):
            raise AuthorizationError("Permission to view AI metrics required")
        
        metrics = await ai_service.get_overall_metrics()
        return metrics
    
    except Exception as e:
        logger.error(f"Get AI metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve AI metrics"
        )

@router.get("/metrics/vision")
async def get_vision_metrics(
    current_user = Depends(get_current_user)
):
    """Get vision analysis metrics"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "view_ai_metrics"):
            raise AuthorizationError("Permission to view AI metrics required")
        
        metrics = await ai_service.get_vision_metrics()
        return metrics
    
    except Exception as e:
        logger.error(f"Get vision metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vision metrics"
        )

@router.get("/metrics/nlp")
async def get_nlp_metrics(
    current_user = Depends(get_current_user)
):
    """Get NLP processing metrics"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "view_ai_metrics"):
            raise AuthorizationError("Permission to view AI metrics required")
        
        metrics = await ai_service.get_nlp_metrics()
        return metrics
    
    except Exception as e:
        logger.error(f"Get NLP metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve NLP metrics"
        )

@router.get("/metrics/voice")
async def get_voice_metrics(
    current_user = Depends(get_current_user)
):
    """Get voice AI metrics"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "view_ai_metrics"):
            raise AuthorizationError("Permission to view AI metrics required")
        
        metrics = await ai_service.get_voice_metrics()
        return metrics
    
    except Exception as e:
        logger.error(f"Get voice metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve voice metrics"
        )

@router.get("/metrics/blockchain")
async def get_blockchain_metrics(
    current_user = Depends(get_current_user)
):
    """Get blockchain transaction metrics"""
    try:
        ai_service = AIService()
        
        # Check permissions
        if not ai_service.has_permission(current_user, "view_ai_metrics"):
            raise AuthorizationError("Permission to view AI metrics required")
        
        metrics = await ai_service.get_blockchain_metrics()
        return metrics
    
    except Exception as e:
        logger.error(f"Get blockchain metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve blockchain metrics"
        )
