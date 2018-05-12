def upload(text):
    doc = to_binary(text)
    return requests.post(
        url + '/upload/',
        data=doc,
        headers={
            'Content-Type': 'binary/octet-stream'
        }).text


def process(data):
    doc = json.dumps(data)
    taskid = requests.get(
        url + '/startTask/',
        headers={
            'Content-Type': 'application/json'
        },
        data=doc).text
    time.sleep(0.2)
    resp = requests.get(url + '/getStatus/' + taskid).text
    print(resp)
    data = json.loads(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.5)
        resp = requests.get(url + '/getStatus/' + taskid).text
        data = json.loads(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]


fileid = upload(texts[0])
out_path = 'out/'
data = {'lpmn': lpmn, 'user': user, 'file': fileid}
data = process(data)
if data == None:
    continue
data = data[0]["fileID"]
content = urllib2.request.urlopen(
    urllib2.Request(url + '/download' + data)).read()
with open(out_path + os.path.basename(file) + '.ccl', "w") as outfile:
    outfile.write(content)
