from rq import Queue
from worker import conn
from Generate_graph import plot_it

q = Queue(connection = conn, default_timeout=5000)
comment = q.enqueue(plot_it)
print(comment)