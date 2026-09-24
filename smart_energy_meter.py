import time
import random
import json
import paho.mqtt.client as mqtt

# -----------------------------
# MQTT Configuration
# -----------------------------
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "smart-energy-meter/demo"

# -----------------------------
# Energy Meter Configuration
# -----------------------------
VOLTAGE = 230.0
ENERGY_KWH = 0.0

# Example electricity tariff
TARIFF_PER_KWH = 6.50


def read_sensor_data():
    """Simulate voltage and current sensor readings."""
    voltage = random.uniform(225, 235)
    current = random.uniform(1, 10)

    return voltage, current


def calculate_power(voltage, current):
    """Calculate apparent power in watts."""
    return voltage * current


def calculate_energy(power, seconds):
    """Calculate energy consumed in kWh."""
    return (power * seconds) / 3_600_000


def calculate_cost(energy):
    """Calculate estimated electricity cost."""
    return energy * TARIFF_PER_KWH


def main():
    global ENERGY_KWH

    client = mqtt.Client()

    print("Connecting to MQTT broker...")

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("Connected successfully.")
    except Exception as error:
        print(f"MQTT connection failed: {error}")
        return

    previous_time = time.time()

    print("\nSmart Energy Meter Started")
    print("-" * 50)

    try:
        while True:
            voltage, current = read_sensor_data()

            power = calculate_power(voltage, current)

            current_time = time.time()
            elapsed_time = current_time - previous_time
            previous_time = current_time

            energy = calculate_energy(power, elapsed_time)
            ENERGY_KWH += energy

            cost = calculate_cost(ENERGY_KWH)

            data = {
                "voltage_V": round(voltage, 2),
                "current_A": round(current, 2),
                "power_W": round(power, 2),
                "energy_kWh": round(ENERGY_KWH, 6),
                "estimated_cost": round(cost, 2)
            }

            payload = json.dumps(data)

            client.publish(MQTT_TOPIC, payload)

            print(
                f"Voltage: {voltage:.2f} V | "
                f"Current: {current:.2f} A | "
                f"Power: {power:.2f} W | "
                f"Energy: {ENERGY_KWH:.6f} kWh | "
                f"Cost: ₹{cost:.2f}"
            )

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nSmart Energy Meter stopped.")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
