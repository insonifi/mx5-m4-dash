import analogio

class LightSensor:
    def __init__(self, pin):
        self.sensor = analogio.AnalogIn(pin)
        self.A = 0.2
        self.avg = 0.0

    def get_avg(self):
        A = self.A
        v = self.get_value()
        self.avg = (1 - self.A) * self.avg + self.A * v

        return int(self.avg)

    def get_value(self):
        return int((self.sensor.value / 65536) * 255)
