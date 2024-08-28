import redis

r = redis.Redis()

for key in r.keys():
    print("\n\n\n " + key + "\n\n")
    for iteration in r.hkeys(key):
        print("iteration {}  :  uuid {}".format(iteration,r.hget(key,iteration)))

