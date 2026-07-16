from orexeva.registry.loader import (
    load_registry,
    save_registry,
    reset_registry,
)

registry = load_registry()

print(registry)

registry["runtime"]["status"] = "running"

save_registry(registry)

print(load_registry())

print(reset_registry())