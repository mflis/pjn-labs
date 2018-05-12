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
    

for sent in first.findall(".//sentence"):
    toks = sent.findall(".//tok")
    anns = tok.findall('ann')

    relevant_anns = []
    for tok in toks:
        anns = tok.findall('ann')
        for ann in anns:
            if int(ann.text) > 0:
                relevant_anns.append((ann, tok.find('orth').text))
    channed = sorted(
        relevant_anns, key=lambda x: (x[0].attrib['chan'], int(x[0].text)))
    grouped = groupby(
        channed, key=lambda x: (x[0].attrib['chan'], int(x[0].text)))
    groups = []
    uniquekeys = []
    for k, g in grouped:
        txt = ' '.join(list(map(itemgetter(1), g)))
        groups.append((k[0], txt))  # Store group iterator as a list
        uniquekeys.append(k)

    print(groups)
