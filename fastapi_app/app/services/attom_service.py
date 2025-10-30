"""
ATTOM Data Solutions API Service
Provides property data from ATTOM API
Official API Documentation: https://api.developer.attomdata.com/docs
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

class AttomService:
    """Service for interacting with ATTOM Data Solutions API"""
    
    def __init__(self):
        # ATTOM API credentials
        self.base_url = "https://api.gateway.attomdata.com"
        self.api_key = os.getenv("ATTOM_API_KEY", "")
        self.email = os.getenv("ATTOM_EMAIL", "info@cygenequities.com")
        
        # Configure headers (as per ATTOM documentation)
        self.headers = {
            "Accept": "application/json",
            "APIKey": self.api_key
        }
    
    def search_properties(
        self, 
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zipcode: Optional[str] = None,
        property_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_sqft: Optional[int] = None,
        max_sqft: Optional[int] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[float] = None,
        limit: int = 50,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Search for properties using ATTOM API
        Official endpoint: /propertyapi/v1.0.0/property/snapshot
        
        Args:
            address: Property address
            city: City name
            state: State code
            zipcode: ZIP code
            property_type: Type of property (e.g., 'sfr', 'condo', 'apartment')
            min_price: Minimum price filter
            max_price: Maximum price filter
            min_sqft: Minimum square footage
            max_sqft: Maximum square footage
            bedrooms: Number of bedrooms
            bathrooms: Number of bathrooms
            limit: Maximum number of results (default: 50, max: 100)
            latitude: Latitude coordinate for radius search
            longitude: Longitude coordinate for radius search
            radius: Radius in miles for location-based search (max: 20)
            
        Returns:
            Dictionary with search results
        """
        try:
            if not self.api_key:
                return {
                    "status": "error",
                    "message": "ATTOM API key is not configured. Please set ATTOM_API_KEY in .env file."
                }
            
            # Build search parameters using official ATTOM API parameter names
            params = {}
            
            # Address-based search
            if address:
                params["address"] = address
            elif address and city and state:
                params["address1"] = address
                params["address2"] = f"{city}, {state}"
            
            # Location-based search
            if latitude and longitude:
                params["latitude"] = latitude
                params["longitude"] = longitude
                if radius:
                    params["radius"] = min(radius, 20)  # Max radius is 20 miles
                else:
                    params["radius"] = 5  # Default radius
            
            # ZIP code search
            if zipcode:
                params["postalCode"] = zipcode
            
            # Property filters
            if property_type:
                params["propertyType"] = property_type
            
            if bedrooms:
                params["beds"] = bedrooms
            
            if bathrooms:
                params["bathsTotal"] = bathrooms
            
            if min_price or max_price:
                params["minMktTtlValue"] = min_price or ""
                params["maxMktTtlValue"] = max_price or ""
            
            if min_sqft or max_sqft:
                params["minUniversalSize"] = min_sqft or ""
                params["maxUniversalSize"] = max_sqft or ""
            
            # Pagination
            params["page"] = 1
            params["pageSize"] = min(limit, 100)  # Max page size is 100
            
            # Remove empty values
            params = {k: v for k, v in params.items() if v is not None and v != ""}
            
            # Make API request to property snapshot endpoint
            url = f"{self.base_url}/propertyapi/v1.0.0/property/snapshot"
            logger.info(f"ATTOM API Request: {url}")
            logger.info(f"ATTOM API Params: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            logger.info(f"ATTOM API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"ATTOM API Response: {data}")
                return {
                    "status": "success",
                    "data": self._normalize_property_data(data)
                }
            else:
                logger.error(f"ATTOM API error: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"ATTOM API error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"ATTOM API request failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to fetch from ATTOM API: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error in ATTOM API: {str(e)}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    def get_property_details(self, property_id: str, address: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed property information by ATTOM ID or address
        Official endpoint: /propertyapi/v1.0.0/property/detail
        
        Args:
            property_id: ATTOM property identifier (attomId)
            address: Alternative - can provide address instead
            
        Returns:
            Dictionary with property details
        """
        try:
            if not self.api_key:
                return {
                    "status": "error",
                    "message": "ATTOM API key is not configured."
                }
            
            # Use detail endpoint
            url = f"{self.base_url}/propertyapi/v1.0.0/property/detail"
            params = {}
            
            if property_id:
                params["attomId"] = property_id
            elif address:
                params["address"] = address
            else:
                return {
                    "status": "error",
                    "message": "Either property_id or address must be provided"
                }
            
            logger.info(f"ATTOM API Request: {url}")
            logger.info(f"ATTOM API Params: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            logger.info(f"ATTOM API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": self._normalize_property_data(data)
                }
            else:
                logger.error(f"ATTOM API error: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"ATTOM API error: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"ATTOM API request failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to fetch property details: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    def _normalize_property_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Normalize ATTOM API response to match our property structure
        Official ATTOM response structure based on documentation
        
        Args:
            data: Raw ATTOM API response
            
        Returns:
            List of normalized property dictionaries
        """
        properties = []
        
        # Check for status and extract property array
        status = data.get("status", {})
        if status.get("code") != 0:
            logger.warning(f"ATTOM API returned non-zero status: {status}")
            return properties
        
        # Extract property array from response
        property_list = data.get("property", [])
        if not isinstance(property_list, list):
            property_list = [property_list] if property_list else []
        
        logger.info(f"Processing {len(property_list)} properties from ATTOM API")
        
        for prop in property_list:
            try:
                # Extract identifier and address data (ATTOM structure places address at top-level)
                identifier = prop.get("identifier", {})
                address = prop.get("address", {})
                
                # Extract property characteristics
                property_char = prop.get("property", {})
                
                # Extract assessment data
                assessment = prop.get("assessment", {})
                assessed_value = assessment.get("assessedValue", {})
                
                # Extract lot data
                lot = prop.get("lot", {})
                
                # Extract sale data (if available)
                sale = prop.get("sale", {})
                sale_amount = sale.get("amount", {}) if sale else {}
                
                # Extract owner data (if available)
                owner = prop.get("owner", {})
                
                # Extract valuation data (if available)
                valuation = prop.get("valuation", {})
                avm = valuation.get("avm", {}) if valuation else {}
                avm_amount = avm.get("amount", {}) if avm else {}
                
                # Build normalized property object based on ATTOM API structure
                normalized = {
                    "id": identifier.get("attomId", identifier.get("id", "")),
                    "street_address": address.get("oneLine", ""),
                    "unit_apt": address.get("unitType", "") or "",
                    "city": address.get("locality", address.get("city", "")),
                    "state": address.get("countrySubd", address.get("state", "")),
                    "zip_code": address.get("postal1", address.get("postalCode", "")),
                    "county": address.get("county", "") or "",
                    "property_type": property_char.get("type", "residential") or "residential",
                    "bedrooms": property_char.get("bedrooms", 0) or 0,
                    "bathrooms": property_char.get("bathsTotal", 0.0) or 0.0,
                    "square_feet": property_char.get("universalSize", 0) or 0,
                    "lot_size": lot.get("lotSize1", 0) or 0,
                    "year_built": property_char.get("yearBuilt", "") or "",
                    "purchase_price": sale_amount.get("value", 0.0) or 0.0,
                    "arv": avm_amount.get("value", 0.0) or 0.0,
                    "repair_estimate": 0.0,  # Not available from ATTOM
                    "holding_costs": 0.0,  # Not available from ATTOM
                    "transaction_type": "wholesale",  # Default
                    "assignment_fee": 0.0,  # Not available from ATTOM
                    "property_description": f"{property_char.get('type', 'property')} property in {address.get('city', '')}, {address.get('state', '')}",
                    "seller_notes": "",
                    "images": [],
                    "status": "available",
                    "source": "attom",
                    "owner_name": owner.get("name", "") or "" if owner else "",
                    "owner_email": "",
                    "owner_phone": "",
                    "attom_data": prop,  # Keep raw data for reference
                    # Additional ATTOM-specific fields
                    "attom_id": identifier.get("attomId", ""),
                    "apn": identifier.get("apn", ""),
                    "fips": identifier.get("fips", ""),
                    "assessed_value": assessed_value.get("tax", {}).get("value", 0.0) or 0.0
                }
                
                properties.append(normalized)
                
            except Exception as e:
                logger.error(f"Error normalizing property data: {str(e)}")
                logger.error(f"Property data: {prop}")
                continue
        
        return properties
    
    def get_market_trends(self, city: str, state: str, zipcode: Optional[str] = None) -> Dict[str, Any]:
        """
        Get market trends for a specific location
        Official endpoint: /v4/salestrend
        
        Args:
            city: City name
            state: State code
            zipcode: ZIP code (optional)
            
        Returns:
            Dictionary with market trend data
        """
        try:
            if not self.api_key:
                return {
                    "status": "error",
                    "message": "ATTOM API key is not configured."
                }
            
            # Use sales trend endpoint
            url = f"{self.base_url}/v4/salestrend"
            params = {}
            
            if zipcode:
                params["postalCode"] = zipcode
            else:
                # Use city and state if no zipcode
                params["city"] = city
                params["state"] = state
            
            logger.info(f"ATTOM API Request: {url}")
            logger.info(f"ATTOM API Params: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            logger.info(f"ATTOM API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "data": data
                }
            else:
                logger.error(f"ATTOM API error: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Failed to fetch market trends: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Market trends request failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Market trends request failed: {str(e)}"
            }

# Create singleton instance
attom_service = AttomService()
