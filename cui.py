import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# opening the WhatsApp chat exported as text in read-mode 
# here, we shall only be dealing with data which does not contain any media
# checking how many lines begin with a date i.e. counting the number of individual whatsapp texts
def startsWithDateTime(s, id):
    if id == 0:
        pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
    else:
        pattern = '(\[)([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), (([0-9][0-9])|([0-9])):([0-9][0-9]):([0-9][0-9]) (AM|PM)(\])' 
    result = re.match(pattern, s)
    if result:
        return True
    return False

# finding the author for the messages
def startsWithAuthor(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        '([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

# spliiting the data-points to get the various components out of a line (Date, Time, Author, Message)
def getDataPoint(line):    
    splitLine = line.split(' - ') 
    dateTime = splitLine[0] 
    date, time = dateTime.split(', ') 
    message = ' '.join(splitLine[1:]) 
    if startsWithAuthor(message):
        splitMessage = message.split(': ') 
        author = splitMessage[0] 
        message = ' '.join(splitMessage[1:]) 
    else:
        author = None
    return date, time, author, message

def get_data(conversationPath, id): 
    parsedData = []
    with open(conversationPath, encoding="utf-8") as fp:
        fp.readline() # Skipping first line of the file (usually contains information about end-to-end encryption)

        messageBuffer = [] # Buffer to capture intermediate output for multi-line messages
        date, time, author = None, None, None # Intermediate variables to keep track of the current message being processed

        while True:
            line = fp.readline() 
            if not line: # Stop reading further if end of file has been reached
                break
            line = line.strip() # Guarding against erroneous leading and trailing whitespaces
            if startsWithDateTime(line, id): # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
                if len(messageBuffer) > 0: # Check if the message buffer contains characters from previous iterations
                    parsedData.append([date, time, author, ' '.join(messageBuffer)]) # Save the tokens from the previous message in parsedData
                messageBuffer.clear() # Clear the message buffer so that it can be used for the next message
                date, time, author, message = getDataPoint(line) # Identify and extract tokens from the line
                messageBuffer.append(message) # Append message to buffer
            else:
                messageBuffer.append(line) # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer

    return parsedData 

def remove_media(df): # takes in a dataframe and removes all the messages which contains media
    counter = 0
    for j in range(2):
        for i in df.index:
            if df["Message"][i] == "<Media omitted>":
                df = df.drop(i)
                counter = counter + 1
    return df, counter 

def remove_lines_with_only_emojis(df): 
    i = 0
    for i in df.index:
        m = df["Message"][i]
        tag = 0
        for each in m:
            for char in each:
                if ord(char) < 3000 and ord(char) != 32:
                    tag = 1
                    break 
            if tag == 1:
                break
        if tag == 0:
            df = df.drop(i)
    return df

def get_pie(df, val = 0):
    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)


    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    author_value_counts = df['Author'].value_counts() # Number of messages per author
    
    wedges, texts, autotexts = ax.pie(author_value_counts, autopct=lambda pct: func(pct, author_value_counts),
                                  textprops=dict(color="w"))

    
    ax.legend(wedges, df['Author'].value_counts().index.tolist(),
          title="Authors",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("Distribution of Messages: A pie")
    if val == 1:
        plt.savefig("AuthorFrequency.png")
    plt.show()
    

def get_bar(df, val = 0):
    type_of_messages = [0,0] # media and non-media
    for j in range(2):
        for i in df.index:
            if df["Message"][i] == "<Media omitted>":
                type_of_messages[0] += 1
            else:
                type_of_messages[1] += 1

    top=[('Media',type_of_messages[0]),('Non-Media',type_of_messages[1])]
    labels, ys = zip(*top)
    xs = np.arange(len(labels)) 
    width = 1

    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels) #Replace default x-ticks with xs, then replace xs with labels
    plt.yticks(ys)
    plt.ylabel("Number of Messages")
    plt.title("Distribution of Media vs Non-Media Messages")
    if val == 1:
        plt.savefig("MessageTypeDistribution.png")
    plt.show()

def get_bar_time(df, val = 0):
    output = [0 for i in range(24)]
    for i in df.index:
        time = int(df['Time'][i][0:2])
        output[time%24] += 1
    top=[(i,output[i]) for i in range(24)]
    labels, ys = zip(*top)
    xs = np.arange(len(labels)) 
    width = 1

    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels) #Replace default x-ticks with xs, then replace xs with labels
    plt.yticks(ys)
    plt.ylabel("Number of Messages")
    plt.title("Distribution of Messages Through Time")
    if val == 1:
        plt.savefig("MessageTimeDistribution.png")
    plt.show()
    

def get_statistics(df, val = 0):
    get_pie(df, val)
    get_bar(df, val)
    get_bar_time(df, val)



if __name__ == '__main__':
    print("Hello World! :P")