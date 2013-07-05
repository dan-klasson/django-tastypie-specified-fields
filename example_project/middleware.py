from django.db import connection 
from django.template import Template, Context
from django.http import HttpResponse

class SQLLogMiddleware:

    def process_response ( self, request, response ): 

        try:
            request.GET['format']
        except:
            return response

        time = 0.0
        for q in connection.queries:
		    time += float(q['time'])
        
        t = Template('''


Total query count: {{ count }}
Total execution time: {{ time }}
{% for sql in sqllog %}
    {{ sql.time }}: {{ sql.sql }}
{% endfor %}
        ''')

        tpl = t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time}))
        content = "%s%s" % ( response.content, tpl)
        content = content.replace('&quot;', '"') # super ugly but does the trick
        
        return HttpResponse(content, content_type="text/text")
