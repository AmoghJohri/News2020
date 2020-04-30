=> This is a tool to deal with WhatsApp Chats and was developed to aid in the course project of DT 216 / News Literacies in the Digital Society.
=> The scope of this tool is to facilitate the process of data-extraction and representation as defined by the project.

How To Run : 
-> Double click on the 'run.sh' file.

How To Use The Tool : 
1. The tool takes an exported WhatsApp Chat (in the form of .txt file) as its input. The 'Input Text File' option can be used to browse and select the required file.
2. Next step is to select the suitable Device Framework (whether the input generated was from a WhatsApp account run on an Android device or an IOS device). The radiobutton next to the suitable choice can be selected.
3. The 'Remove Emojis' radiobutton can be selected to remove all the texts which contain only Emojis.
4. The 'Get Statistics' radiobutton can be selected, this will provide the user with various statistics (at the end of the computation) such as - 'Distribution of Messages With Respect To Authors', etc in the form of graphs.
5. The 'Save Statistics' radiobutton can be selected to save all the graphs created in the above process.
6. The 'Get CSV File' button can be clicked to begin the computation. At this point, the tool fetches the input file, carries out the necessary computation and saves the output as a 'csv' file (with the same name as the input file and in the same directory as well).
    The CSV file thus formed contains the following four columns : 
    Date, Time, Author and Message
7. In the case of 'Save Statistics' radio button being selected, the graphs are stored in the form of png images in the same directory as that of the tool.
