
configs = config_default.configs

try:
	import config_verride
	configs = merge(configs, config_override.configs)
except ImportError:
	pass