f= open("config.txt","w+")

img_url ="http://192.168.0.106:8080/shot.jpg"
openalpr_apikey = "sk_84ab70b5d8b123bb51c0e466"

store = {'img_url':img_url,'openalpr_apikey':openalpr_apikey}
print(store)
for i in store:
    f.write('{0:s} : {1:s}\n' .format(i,store[i]))
f.close()



f= open("config.txt","r")
arr = {}
for _ in range(0,2):
    result = f.readline()
    arr[result.split(' : ')[0]] = result.split(' : ')[-1].split('\n')[0]
print(arr)
f.close()