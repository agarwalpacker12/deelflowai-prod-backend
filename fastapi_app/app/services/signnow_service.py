"""
SignNow API Service
Provides electronic signature functionality using SignNow API
Official API Documentation: https://api.signnow.com/docs
"""

import requests
import os
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

logger = logging.getLogger(__name__)

class SignNowService:
    """Service for interacting with SignNow API"""
    
    def __init__(self):
        # SignNow API credentials
        self.base_url = "https://api.signnow.com"  # Production
        # self.base_url = "https://api-eval.signnow.com"  # Sandbox for testing
        
        # OAuth 2.0 credentials
        self.client_id = os.getenv("SIGNNOW_CLIENT_ID", "")
        self.client_secret = os.getenv("SIGNNOW_CLIENT_SECRET", "")
        self.username = os.getenv("SIGNNOW_USERNAME", "info@cygenequities.com")
        self.password = os.getenv("SIGNNOW_PASSWORD", "Revelation21v21$")
        
        # Store access token
        self.access_token = None
        self.token_type = "Bearer"
        
        # Configure headers
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def authenticate(self) -> bool:
        """
        Authenticate with SignNow API using OAuth 2.0
        SignNow OAuth 2.0 authentication flow
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Check if we have Client ID and Secret
            if not self.client_id or not self.client_secret:
                logger.error("SignNow Client ID or Client Secret is not configured")
                logger.error("Please add SIGNNOW_CLIENT_ID and SIGNNOW_CLIENT_SECRET to .env file")
                logger.error("You can get these from: https://app.signnow.com/webapp/api-dashboard/keys")
                return False
            
            # OAuth 2.0 authentication endpoint
            url = f"{self.base_url}/oauth2/token"
            
            # Prepare OAuth request
            auth_payload = {
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
                "scope": "user"
            }
            
            # Basic Auth header
            import base64
            credentials = f"{self.client_id}:{self.client_secret}"
            credentials_base64 = base64.b64encode(credentials.encode()).decode()
            
            auth_headers = {
                "Authorization": f"Basic {credentials_base64}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            logger.info(f"SignNow OAuth Request: {url}")
            
            response = requests.post(url, headers=auth_headers, data=auth_payload, timeout=30)
            
            logger.info(f"SignNow Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Store access token
                self.access_token = data.get("access_token")
                self.token_type = data.get("token_type", "Bearer")
                
                # Update headers with access token
                self.headers["Authorization"] = f"{self.token_type} {self.access_token}"
                
                logger.info(f"SignNow authenticated successfully")
                logger.info(f"Access Token: {self.access_token[:20]}...")
                
                return True
            else:
                logger.error(f"SignNow OAuth failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"SignNow authentication error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get authenticated user information
        
        Returns:
            Dictionary with user information
        """
        try:
            # Try to authenticate first if we don't have a token
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication failed"
                    }
            
            # SignNow doesn't expose a simple user endpoint
            # Return authenticated status since we have a valid access token
            return {
                "status": "success",
                "data": {
                    "message": "Authentication successful",
                    "authenticated": True,
                    "token_type": self.token_type,
                    "username": self.username
                }
            }
                
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def upload_document(self, file_path: str, document_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a document to SignNow
        
        Args:
            file_path: Path to the document file to upload
            document_name: Optional custom name for the document
            
        Returns:
            Dictionary with document upload result including document ID
        """
        try:
            # Authenticate if needed
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication required"
                    }
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }
            
            # Use document_name or extract from file path
            if not document_name:
                document_name = os.path.basename(file_path)
            
            # SignNow document upload endpoint - requires multipart form data
            url = f"{self.base_url}/api/v1/document"
            
            # Prepare multipart form data
            with open(file_path, 'rb') as f:
                files = {
                    'file': (document_name, f, 'application/pdf')  # Adjust content type as needed
                }
                
                # Remove Content-Type from headers for multipart upload (requests sets it automatically)
                upload_headers = {
                    "Authorization": self.headers.get("Authorization")
                }
                
                logger.info(f"Uploading document to SignNow: {document_name}")
                response = requests.post(url, headers=upload_headers, files=files, timeout=60)
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Document uploaded successfully: {data.get('id', 'Unknown ID')}")
                return {
                    "status": "success",
                    "data": data
                }
            else:
                logger.error(f"Failed to upload document: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}: Failed to upload document",
                    "data": response.text
                }
                
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }
    
    def create_document(self, document_name: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new document in SignNow (legacy method - use upload_document for file uploads)
        
        Args:
            document_name: Name of the document
            file_path: Path to document file (optional)
            
        Returns:
            Dictionary with document creation result
        """
        # If file_path is provided, use upload_document instead
        if file_path:
            return self.upload_document(file_path, document_name)
        
        try:
            # Authenticate if needed
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication required"
                    }
            
            # SignNow document creation endpoint (for empty documents)
            url = f"{self.base_url}/api/v1/document"
            
            payload = {
                "name": document_name,
                "template": False
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                data = response.json()
                return {
                    "status": "success",
                    "data": data
                }
            else:
                logger.error(f"Failed to create document: {response.status_code}")
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}",
                    "data": response.text
                }
                
        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_documents(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get list of documents
        
        Args:
            limit: Maximum number of documents to return
            
        Returns:
            Dictionary with document list
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication required"
                    }
            
            url = f"{self.base_url}/api/v1/document"
            params = {"limit": limit}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": data
                }
            else:
                logger.error(f"Failed to get documents: {response.status_code}")
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}",
                    "data": response.text
                }
                
        except Exception as e:
            logger.error(f"Error getting documents: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def invite_signers(self, document_id: str, signers: List[Dict[str, Any]], 
                       subject: Optional[str] = None, message: Optional[str] = None) -> Dict[str, Any]:
        """
        Send document invitation to signers
        
        Args:
            document_id: SignNow document ID
            signers: List of signer dictionaries with keys: email, order (optional)
            subject: Email subject (optional)
            message: Email message (optional)
            
        Returns:
            Dictionary with invitation result
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication required"
                    }
            
            # SignNow invite endpoint
            url = f"{self.base_url}/api/v1/document/{document_id}/invite"
            
            # Format signers correctly
            formatted_signers = []
            for idx, signer in enumerate(signers):
                formatted_signer = {
                    "email": signer.get("email"),
                    "order": signer.get("order", idx + 1),
                    "role_id": signer.get("role_id", "Signer"),  # Default role
                    "role": signer.get("role", "Signer")
                }
                formatted_signers.append(formatted_signer)
            
            payload = {
                "to": formatted_signers,
                "subject": subject or "Please sign this document",
                "message": message or "Please review and sign the attached document."
            }
            
            logger.info(f"Sending invitation for document {document_id} to {len(formatted_signers)} signer(s)")
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Invitation sent successfully")
                return {
                    "status": "success",
                    "data": data
                }
            else:
                logger.error(f"Failed to send invitation: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}: Failed to send invitation",
                    "data": response.text
                }
                
        except Exception as e:
            logger.error(f"Error sending invitation: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }
    
    def send_document_for_signature(self, document_id: str, signer_email: str, 
                                   subject: Optional[str] = None, message: Optional[str] = None) -> Dict[str, Any]:
        """
        Send document for signature (legacy method - use invite_signers for multiple signers)
        
        Args:
            document_id: SignNow document ID
            signer_email: Email address of the signer
            subject: Email subject (optional)
            message: Email message (optional)
            
        Returns:
            Dictionary with sending result
        """
        # Use the new invite_signers method
        return self.invite_signers(
            document_id=document_id,
            signers=[{"email": signer_email}],
            subject=subject,
            message=message
        )
    
    def get_document_status(self, document_id: str) -> Dict[str, Any]:
        """
        Get document status and information
        
        Args:
            document_id: SignNow document ID
            
        Returns:
            Dictionary with document status information
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication required"
                    }
            
            # SignNow document status endpoint
            url = f"{self.base_url}/api/v1/document/{document_id}"
            
            logger.info(f"Getting status for document: {document_id}")
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": data
                }
            else:
                logger.error(f"Failed to get document status: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}: Failed to get document status",
                    "data": response.text
                }
                
        except Exception as e:
            logger.error(f"Error getting document status: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def download_document(self, document_id: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Download a document from SignNow
        
        Args:
            document_id: SignNow document ID
            file_path: Optional path to save the downloaded file
            
        Returns:
            Dictionary with download result including file content or saved path
        """
        try:
            if not self.access_token:
                if not self.authenticate():
                    return {
                        "status": "error",
                        "message": "Authentication required"
                    }
            
            # SignNow document download endpoint
            url = f"{self.base_url}/api/v1/document/{document_id}/download"
            
            logger.info(f"Downloading document: {document_id}")
            response = requests.get(url, headers=self.headers, timeout=60, stream=True)
            
            if response.status_code == 200:
                # If file_path provided, save to file
                if file_path:
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    logger.info(f"Document saved to: {file_path}")
                    return {
                        "status": "success",
                        "data": {
                            "message": "Document downloaded successfully",
                            "file_path": file_path,
                            "document_id": document_id
                        }
                    }
                else:
                    # Return file content
                    return {
                        "status": "success",
                        "data": {
                            "content": response.content,
                            "content_type": response.headers.get("Content-Type"),
                            "document_id": document_id
                        }
                    }
            else:
                logger.error(f"Failed to download document: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}: Failed to download document",
                    "data": response.text
                }
                
        except Exception as e:
            logger.error(f"Error downloading document: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to SignNow API
        
        Returns:
            Dictionary with connection test result
        """
        try:
            # Check configuration
            if not self.client_id or not self.client_secret:
                return {
                    "status": "error",
                    "message": "SignNow credentials are not configured. Please set SIGNNOW_CLIENT_ID and SIGNNOW_CLIENT_SECRET in .env file.",
                    "authenticated": False,
                    "config_required": True
                }
            
            # Try to authenticate
            auth_result = self.authenticate()
            
            if auth_result:
                # Get user info to verify
                user_info = self.get_user_info()
                
                return {
                    "status": "success",
                    "message": "SignNow API connection successful",
                    "authenticated": True,
                    "user": user_info.get("data", {}),
                    "access_token": self.access_token[:20] + "..." if self.access_token else None
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to authenticate with SignNow API. Please check your credentials.",
                    "authenticated": False
                }
                
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}"
            }

# Create singleton instance
signnow_service = SignNowService()

