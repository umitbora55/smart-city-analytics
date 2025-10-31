"""
Real data fetcher from external APIs and datasets
"""
import os
import requests
import time
from typing import Dict, Optional, List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class WeatherDataFetcher:
    """Fetch real weather data from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.last_call_time = 0
        self.min_interval = 60  # Minimum 60 seconds between calls (API limit)
        self.cache = {}
        self.cache_duration = 600  # Cache for 10 minutes
    
    def fetch_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch weather data for given coordinates
        Implements caching and rate limiting
        """
        if not self.api_key or self.api_key == 'your_api_key_here':
            return None
        
        # Check cache
        cache_key = f"{lat:.2f},{lon:.2f}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        # Rate limiting
        time_since_last_call = time.time() - self.last_call_time
        if time_since_last_call < self.min_interval:
            return None  # Use simulated data instead
        
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            self.last_call_time = time.time()
            
            # Transform to our schema
            weather_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed']
            }
            
            # Cache the data
            self.cache[cache_key] = (weather_data, time.time())
            
            return weather_data
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None


class DatasetLoader:
    """Load and process static datasets (traffic, energy)"""
    
    def __init__(self, dataset_path: str = "../../data/raw"):
        self.dataset_path = dataset_path
        self.datasets = {}
    
    def load_traffic_dataset(self) -> Optional[List[Dict]]:
        """
        Load traffic dataset from local files
        In production, this would load from Kaggle or other sources
        """
        # Placeholder - will be implemented when we download datasets
        return None
    
    def load_energy_dataset(self) -> Optional[List[Dict]]:
        """
        Load energy consumption dataset
        In production, this would load from local files or APIs
        """
        # Placeholder - will be implemented when we download datasets
        return None


class HybridDataManager:
    """
    Manages hybrid data generation strategy
    Combines real API data with simulated data
    """
    
    def __init__(self):
        self.weather_fetcher = WeatherDataFetcher()
        self.dataset_loader = DatasetLoader()
        self.real_data_enabled = os.getenv('REAL_DATA_ENABLED', 'true').lower() == 'true'
        self.hybrid_ratio = float(os.getenv('HYBRID_RATIO', '0.7'))
        
        # Statistics
        self.stats = {
            'real_data_count': 0,
            'simulated_data_count': 0,
            'api_errors': 0
        }
    
    def get_weather_data(self, lat: float, lon: float, simulated_data: Dict) -> Dict:
        """
        Get weather data - real if available, otherwise simulated
        """
        if self.real_data_enabled:
            real_data = self.weather_fetcher.fetch_weather(lat, lon)
            if real_data:
                self.stats['real_data_count'] += 1
                return {**simulated_data, **real_data}
        
        self.stats['simulated_data_count'] += 1
        return simulated_data
    
    def print_statistics(self):
        """Print data source statistics"""
        total = self.stats['real_data_count'] + self.stats['simulated_data_count']
        if total > 0:
            real_percentage = (self.stats['real_data_count'] / total) * 100
            print(f"\nData Source Statistics:")
            print(f"Real data: {self.stats['real_data_count']} ({real_percentage:.1f}%)")
            print(f"Simulated: {self.stats['simulated_data_count']} ({100-real_percentage:.1f}%)")
            print(f"API errors: {self.stats['api_errors']}")
