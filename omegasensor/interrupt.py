import RPi.GPIO as GPIO


def setup_interrupt(pin, callback):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback)


def remove_interrupt(pin):
    GPIO.remove_event_detect(pin)
    GPIO.cleanup()

