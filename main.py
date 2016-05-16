#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Todo


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
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("chat.html")

class SendHandler(BaseHandler):
    def validation(self, input):
        input = input.replace("<", "")
        input = input.replace("</", "")
        return input

    def post(self):
        task = self.request.get("task")

        task = self.validation(task)

        task = Todo(task=task)
        task.put()

        return self.render_template("sporocilo-poslano.html")


class ShowAllHandler(BaseHandler):
    def get(self):
        tasks = Todo.query().order(-Todo.nastanek).fetch()

        view_vars = {
            "tasks": tasks
        }

        return self.render_template("prikazi_sporocila.html", view_vars)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, task_id):
        task = Todo.get_by_id(int(task_id))

        view_vars = {
            "task": task
        }

        return self.render_template("posamezno_sporocilo.html", view_vars)


class EditHandler(BaseHandler):
    def get(self, task_id):
        task = Todo.get_by_id(int(task_id))

        view_vars = {
            "task": task
        }

        return self.render_template("uredi_sporocilo.html", view_vars)

    def validation(self, input):
        input = input.replace("<", "")
        input = input.replace("</", "")
        return input

    def post(self, task_id):
        task = Todo.get_by_id(int(task_id))
        task.task = self.request.get("task")
        task.task = self.validation(task.task)
        task.put()

        self.redirect("/task/" + task_id)


class DeleteHandler(BaseHandler):
    def get(self, task_id):
        task = Todo.get_by_id(int(task_id))

        view_vars = {
            "task": task
        }

        return self.render_template("izbrisi_sporocilo.html", view_vars)

    def post(self, task_id):
        task = Todo.get_by_id(int(task_id))
        task.key.delete()

        self.redirect("/prikazi_sporocila")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/poslji-sporocilo', SendHandler),
    webapp2.Route('/prikazi_sporocila', ShowAllHandler),
    webapp2.Route('/task/<task_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/task/<task_id:\d+>/uredi', EditHandler),
    webapp2.Route('/task/<task_id:\d+>/izbrisi', DeleteHandler),
], debug=True)
