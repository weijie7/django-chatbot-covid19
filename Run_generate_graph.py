from rq import Queue
from worker import conn
from generate_graph import plot_it

q = Queue(connection = conn)
comment = q.enqueue(plot_it)
print(comment)