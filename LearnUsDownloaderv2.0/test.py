# import threading
# import time
# import random
# import queue
# import sys

# # a downloading thread


# def worker(path, total, q):
#     size = 0
#     while size < total:
#         dt = random.randint(1, 3)
#         time.sleep(dt)
#         ds = random.randint(1, 5)
#         size = size + ds
#         if size > total:
#             size = total
#         q.put(("update", path, total, size))
#     q.put(("done", path))

# # the reporting thread


# def reporter(q, nworkers):
#     status = {}
#     while nworkers > 0:
#         msg = q.get()
#         if msg[0] == "update":
#             path, total, size = msg[1:]
#             status[path] = (total, size)
#             # update the screen here
#             show_progress(status)
#         elif msg[0] == "done":
#             nworkers = nworkers - 1
#     print("")


# def show_progress(status):
#     line = ""
#     for path in status:
#         (total, size) = status[path]
#         line = line + "%s: %3d/%d   " % (path, size, total)
#     sys.stdout.write("\r"+line)
#     sys.stdout.flush()


# def main():
#     q = queue.Queue()
#     w1 = threading.Thread(target=worker, args=("abc", 30, q))
#     w2 = threading.Thread(target=worker, args=("foobar", 25, q))
#     w3 = threading.Thread(target=worker, args=("bazquux", 16, q))
#     r = threading.Thread(target=reporter, args=(q, 3))
#     for t in [w1, w2, w3, r]:
#         t.start()
#     for t in [w1, w2, w3, r]:
#         t.join()


# main()

print(format(12.1233, "0>6.2f"))
