#little functions needed across all 
import email


def striptext(filepath):

    # init
    try:
        fp = open(filepath, 'r', encoding="ISO-8859-1")
    except:
        return []
    string = fp.read()
    message = email.message_from_string(string)
    if message['Subject'] is not None:
        subject = message['Subject'].split()
    else:
        subject = ' '
    if message['From'] is not None:
        sender = message['From'].split()
    else:
        sender = ' '
    email_text = []
    fp.close()

    # go through email body
    if message.is_multipart():
        for payload in message.get_payload():
            payload = str(payload).split("\n")
            poplist = []
            count = 0
            for i in range(len(payload)):
                # delete useless stuff
                if payload[i][:13] == "Content-Type:":
                    count = 4
                if count > 0:
                    poplist.append(i) 
                    count -= 1
                    continue
                if payload[i][:5] == "-----":
                    poplist.append(i)
            poplist.sort(reverse=True)
            for i in poplist:
                payload.pop(i)
            # add the result to list
            email_text += payload  
    else:
        payload = message.get_payload()
        email_text = str(payload).split("\n")
    
    # split words and take out tags
    output = []
    tag = False
    for line in email_text:
        line = line.split()
        for word in line:
            if len(word) > 20:
                continue
            if word[0] == '<':
                tag = True
            if '>' in word:
                tag = False
            elif tag is False:
                # don't want numbers
                if word[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    continue
                output.append(word)
    
    # add subject and email
    output += sender
    output += subject
    # clean word 
    for i in range(len(output)):
        output[i] = clean_word(output[i])
    return output



def delete_dup(input_list):
    #sort and remove duplicates from a list
    input_list.sort()
    i = 0
    old = -1
    output_list = []
    while(i<len(input_list)):
        if input_list[i] != old:
            output_list.append(input_list[i])
            old = input_list[i]
        i += 1
       
    return output_list
    

def clean_word(word):
    #clean all the unnessary punctuation from the word
    punctuation = [',','.','/','?','!',"'",'"',':',';','*','(',')','[',']','-','–']
    for i in punctuation:
        try:
            word = word.replace(i,'')
        except:
            print ("clean_word error:",word)
            continue
        
    word = word.lower()
    if len(word)>=4:
    #take out s and es in the end
        if word[-2:] == 'es':
            word = word[:-2]
        elif word[-2:]=='ss':
            pass
        elif word[-1] == 's':
            word = word[:-1]
        

    return word
