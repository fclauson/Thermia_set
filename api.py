from ThermiaOnlineAPI import Thermia

class ThermiaHeatPumpAPI:
    def __init__(self, username, password):
        self._client = Thermia(username, password)

    def set_register(self, register, value):
        # Using the provided set_register method
        return self._client.set_register(register, value)

    def get_register(self, register):
        # Using the provided get_register method
        return self._client.get_register(register)
