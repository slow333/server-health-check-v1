from . import contents_routes, auth, blog, health_check, server

def init_app(app):
  app.register_blueprint(auth.bp)
  app.register_blueprint(blog.bp)
  app.register_blueprint(server.bp)
  app.register_blueprint(health_check.bp)

  app.register_blueprint(contents_routes.bp)
