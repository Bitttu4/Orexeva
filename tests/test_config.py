from orexeva.config import Config

config = Config()

print(config.all())

config.set("theme", "dark")

config.save()

print(config.get("theme"))

config.reset()

print(config.get("theme"))