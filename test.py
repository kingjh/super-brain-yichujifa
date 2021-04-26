import time

start_s = time.time()
time.sleep(1)
end_s = time.time()
m, s = divmod(end_s - start_s, 60)
h, m = divmod(m, 60)
duration = "%02d:%02d:%02d" % (h, m, s)
print(duration)