from . import contents_routes, auth, health_server

def init_app(app):
  app.register_blueprint(auth.bp)
  app.register_blueprint(health_server.bp)

  app.register_blueprint(contents_routes.bp)
