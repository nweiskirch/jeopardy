# the import section
import webapp2
import jinja2
from google.appengine.api import urlfetch
import os
import json
from google.appengine.api import users

# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# def make_clue(question, answer, category, value):
#     return {
#         'question': question,
#         'answer': answer,
#         'category': category,
#         'value': value,
#     }
#
# clue1 = make_clue('Apple\'s Leopard is a type of OS, one of these', 'an operating system', 'Computer Lingo', 200)
# clue2 = make_clue('The "HT" in both HTTP & HTML stands for this', 'hypertext', 'Computer Lingo', 400)
# clue3 = make_clue('If your machine is being controlled by someone else, it may have been taken over by this 3-letter piece of malware', 'a bot', 'Computer Lingo', 600)
# clue4 = make_clue('To set up the pictures & clips on my blog, I might need a VGA, this "array"', 'video graphics', 'Computer Lingo', 800)
# clue5 = make_clue('Send me that report as a PDF, this "format"', 'portable document format', 'Computer Lingo', 1000)
# clue6 = make_clue('We won\'t ruin the plot for you, but watch out for Uncle Scar when you see this show based on a Disney film', 'Lion King', 'Killer Musicals', 200)
#
# clues = [clue1, clue2, clue3, clue4, clue5]

def get_random_clues(num):
    random_url = 'https://jservice.io/api/random?count=' + str(num)
    random_resp = urlfetch.Fetch(random_url).content
    return json.loads(random_resp)

def get_clues(num, category_id):
    clue_url = 'https://jservice.io/api/clues?category=' + str(category_id)
    clue_resp = urlfetch.Fetch(clue_url).content
    return json.loads(clue_resp)[0:num]

def get_categories(num):
    category_url = 'https://jservice.io/api/categories?count=' + str(num)
    category_resp = urlfetch.Fetch(category_url).content
    return json.loads(category_resp)

# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/quiz.html')
        values = {'clues': get_random_clues(5)}
        self.response.write(index_template.render(values))

class CategoriesPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/categories.html')
        values = {
            'categories': get_categories(10),
            'user': user,
            'login_url': users.create_login_url('/categories'),
            'logout_url': users.create_logout_url('/categories'),
        }
        self.response.write(index_template.render(values))

class QuizPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        category_param = self.request.get('category_param')
        index_template = JINJA_ENV.get_template('templates/quiz.html')
        values = {'clues': get_clues(5, category_param)}
        self.response.write(index_template.render(values))

# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/categories', CategoriesPage),
    ('/quiz', QuizPage)
], debug=True)
