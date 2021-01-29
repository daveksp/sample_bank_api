def initialize_extensions(app, extensions):
    """Initializes all flask extensions"""
    for extension in extensions:
        extension.init_app(app)
