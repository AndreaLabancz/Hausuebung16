import os

import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


# handlers
class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("homepage.html", params={})

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("aboutme.html", params={})

class ProjectsHandler(BaseHandler):
    def get(self):
        return self.render_template("myprojects.html", params={})

class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html", params={})


class ContactHandler(BaseHandler):
    def get(self):
         return self.render_template("contact.html", params={})


# URLs
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/myprojects', ProjectsHandler),
    webapp2.Route('/blog', BlogHandler),
    webapp2.Route('/contact', ContactHandler),
], debug=True)

# run on server
localhost = True  # True: non-GAE localhost server; False: GAE on either localhost or on Google Cloud
if localhost:
    def main():
        from paste import httpserver
        from paste.cascade import Cascade
        from paste.urlparser import StaticURLParser

        assets_dir = os.path.join(os.path.dirname(__file__))
        static_app = StaticURLParser(directory=assets_dir)

        web_app = Cascade([app, static_app])
        httpserver.serve(web_app, host='localhost', port='8080')


    if __name__ == '__main__':
        main()
