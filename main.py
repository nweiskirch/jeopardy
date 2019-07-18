# the import section
import webapp2
import jinja2
import os

# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def make_clue(question, answer, category, value):
    return {
        'question': question,
        'answer': answer,
        'category': category,
        'value': value,
    }

clue1 = make_clue('Apple\'s Leopard is a type of OS, one of these', 'an operating system', 'Computer Lingo', 200)
clue2 = make_clue('The "HT" in both HTTP & HTML stands for this', 'hypertext', 'Computer Lingo', 400)
clue3 = make_clue('If your machine is being controlled by someone else, it may have been taken over by this 3-letter piece of malware', 'a bot', 'Computer Lingo', 600)
clue4 = make_clue('To set up the pictures & clips on my blog, I might need a VGA, this "array"', 'video graphics', 'Computer Lingo', 800)
clue5 = make_clue('Send me that report as a PDF, this "format"', 'portable document format', 'Computer Lingo', 1000)

clues = [clue1, clue2, clue3, clue4, clue5]

# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/quiz.html')
        values = {'clues': clues}
        self.response.write(index_template.render(values))

# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
