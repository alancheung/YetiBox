from time import sleep
import requests

class HomeAssistantGateway:
    """A class that communicates with a home assistant library"""
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get_state(self, entity_id: str) -> dict:
        url = f"{self.base_url}/api/states/{entity_id}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def toggle_light(self) -> None:
        entity_payload = {
            "entity_id": "light.office_one",
        }
        self._call_service(domain="light", service="turn_off", data=entity_payload)

        sleep(3)
        
        self._call_service(domain="light", service="turn_on", data=entity_payload)

    def _call_service(self, domain: str, service: str, data: dict) -> list:
        """Triggers an automation action inside Home Assistant using a one-off POST request."""
        url = f"{self.base_url}/api/services/{domain}/{service}"
        
        # Making an independent HTTP request without a Session object
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()