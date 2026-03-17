"""
Cliente para consumir la API del Banco Central de la República Argentina (BCRA)
Documentación oficial: https://www.bcra.gob.ar/apis-banco-central/
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BCRAClient:
    """Cliente para interactuar con la API del BCRA"""
    
    BASE_URL = "https://api.bcra.gob.ar"
    
    # IDs de las principales variables según la documentación del BCRA
    VARIABLES = {
        "reservas": 1,              # Reservas Internacionales
        "tipo_cambio_oficial": 4,   # Tipo de Cambio de Referencia (USD)
        "inflacion_mensual": 31,    # Variación mensual IPC
        "inflacion_anual": 32,      # Variación interanual IPC
        "badlar": 7,                # Tasa BADLAR
        "plazo_fijo": 10,           # Tasa de plazo fijo
        "lebac": 6,                 # Tasa de LELIQ (ex-LEBAC)
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Dashboard BCRA - UBA Ciencia Política'
        })
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Realiza una petición a la API del BCRA
        
        Args:
            endpoint: Endpoint de la API
            params: Parámetros de la query
            
        Returns:
            Respuesta JSON o None si hay error
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al consultar API del BCRA: {e}")
            return None
    
    def get_datos_variable(
        self, 
        variable_id: int, 
        desde: Optional[str] = None,
        hasta: Optional[str] = None
    ) -> List[Dict]:
        """
        Obtiene datos de una variable específica del BCRA
        
        Args:
            variable_id: ID de la variable según BCRA
            desde: Fecha inicial (formato YYYY-MM-DD)
            hasta: Fecha final (formato YYYY-MM-DD)
            
        Returns:
            Lista de diccionarios con los datos
        """
        # Si no se especifican fechas, traer últimos 30 días
        if not hasta:
            hasta = datetime.now().strftime("%Y-%m-%d")
        if not desde:
            desde = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        endpoint = f"estadisticas/v1/DatosVariable/{variable_id}/{desde}/{hasta}"
        
        data = self._make_request(endpoint)
        
        if data and 'results' in data:
            logger.info(f"Variable {variable_id}: {len(data['results'])} registros obtenidos")
            return data['results']
        
        return []
    
    def get_reservas(self, desde: str = None, hasta: str = None) -> List[Dict]:
        """Obtiene datos de Reservas Internacionales"""
        return self.get_datos_variable(self.VARIABLES['reservas'], desde, hasta)
    
    def get_tipo_cambio(self, desde: str = None, hasta: str = None) -> List[Dict]:
        """Obtiene datos del Tipo de Cambio USD"""
        return self.get_datos_variable(self.VARIABLES['tipo_cambio_oficial'], desde, hasta)
    
    def get_inflacion_mensual(self, desde: str = None, hasta: str = None) -> List[Dict]:
        """Obtiene datos de Inflación Mensual"""
        return self.get_datos_variable(self.VARIABLES['inflacion_mensual'], desde, hasta)
    
    def get_badlar(self, desde: str = None, hasta: str = None) -> List[Dict]:
        """Obtiene datos de tasa BADLAR"""
        return self.get_datos_variable(self.VARIABLES['badlar'], desde, hasta)
    
    def get_plazo_fijo(self, desde: str = None, hasta: str = None) -> List[Dict]:
        """Obtiene datos de tasa de plazo fijo"""
        return self.get_datos_variable(self.VARIABLES['plazo_fijo'], desde, hasta)
    
    def get_principales_variables(self) -> Dict:
        """
        Obtiene las principales variables para el dashboard
        
        Returns:
            Diccionario con todas las variables principales
        """
        logger.info("Obteniendo principales variables del BCRA...")
        
        return {
            "reservas": self.get_reservas(),
            "tipo_cambio": self.get_tipo_cambio(),
            "inflacion_mensual": self.get_inflacion_mensual(),
            "badlar": self.get_badlar(),
            "plazo_fijo": self.get_plazo_fijo(),
        }
    
    def get_ultimos_valores(self) -> Dict:
        """
        Obtiene solo el último valor de cada variable principal
        
        Returns:
            Diccionario con los últimos valores
        """
        logger.info("Obteniendo últimos valores de variables principales...")
        
        # Obtener datos de los últimos 7 días para asegurar tener valores
        desde = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        hasta = datetime.now().strftime("%Y-%m-%d")
        
        resultado = {}
        
        for nombre, variable_id in self.VARIABLES.items():
            datos = self.get_datos_variable(variable_id, desde, hasta)
            if datos:
                # Tomar el último valor disponible
                ultimo = datos[-1]
                resultado[nombre] = {
                    "valor": ultimo.get("valor"),
                    "fecha": ultimo.get("fecha")
                }
        
        return resultado


# Script de prueba
if __name__ == "__main__":
    print("=" * 60)
    print("Probando cliente de API del BCRA")
    print("=" * 60)
    
    client = BCRAClient()
    
    # Probar últimos valores
    print("\n📊 Últimos valores de variables principales:\n")
    ultimos = client.get_ultimos_valores()
    
    for variable, data in ultimos.items():
        if data:
            print(f"{variable.upper():20} | Valor: {data['valor']:>15} | Fecha: {data['fecha']}")
    
    # Probar obtener serie de tipo de cambio
    print("\n" + "=" * 60)
    print("💵 Serie de Tipo de Cambio (últimos 10 días):\n")
    
    desde = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    tipo_cambio = client.get_tipo_cambio(desde=desde)
    
    for registro in tipo_cambio[-5:]:  # Mostrar últimos 5
        print(f"Fecha: {registro['fecha']} | USD: ${registro['valor']}")
    
    print("\n✅ Cliente funcionando correctamente!")
