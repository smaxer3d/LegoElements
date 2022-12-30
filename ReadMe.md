# Lego elements

## Introduction

So, you're rebuilding a Lego-set, that might be missing a few pieces.  
Take it all apart, split by color, sort the pieces,
count them (check them as you go) and check with the parts-list if you're missing something.
If so, write down the number of pieces you're missing and the number of the piece.

Great!  
Now, let's order the pieces!

First, the number that you took from the parts-list is not a part-number, but an 'element-id'.  
Some web-shops don't accept the element-id, but the actual part-number and the color.  
Since we can't derive the part-number from the element-id and it's hard to exactly name the color of the piece, 
we use the [Rebrickable API](https://rebrickable.com/api/) to get this information.
We also get a description and a link to an image of the part while we're at it.  
*Btw, the 1-second delay between API-calls is respected*

Second, an element-id, part-number, color and description doesn't help you much when you are at a shop where they sell second-hand Lego that you have to gather from large boxes of mixed pieces.  
That's where that link to an image comes in!

## Put it to use

Personally, I like to write a note.  
Especially when there is little room on the table with all the pieces spread out.  
![Note](https://github.com/smaxer3d/LegoElements/blob/master/img/note.png)  
And type it into a txt-file later:

### 1. txt-file
  
'Lego elements' expects a tab between the quantity and the element-id.  
The filename should be ```[set_nr] - [set_name].txt```, as 'Lego elements' can use the ```set_nr``` to get additional info.  
```set_name``` is not used, so it can be the name of the set or a description.
```
1	4558952
1	6035617
1	4529236
1	302426
1	4106552
1	366026
1	4560182
1	6055172
4	4211398
6	6134378
5	6123809
2	4211397
2	4211413
1	4211063
1	4620077
1	6052266
1	6093529
```
### 2. csv-file

'Lego elements' gets the info (Part, Color, Description and Image) from the Rebrickable API line by line and
writes it into a csv-file with the same name as the txt-file (without the extension) in the same folder.  
This file is perfect for working with spreadsheets or uploading to web-shops or online parts-list imports.

### 3. 'Lego checklist.html'

Finally, 'Lego elements' gets all the csv-files from the directory (to combine all lists into 1 html-file),
gets extra info per csv-file and puts it in a nice web-page and writes it to the same folder.  
From your browser, you can use it directly or print it (to PDF).  
The 'Remark'-column may be used to note the web-shop(s) that were used to order the parts.
Or, to note that the part that you find in the shop is slightly damaged, for instance.

![PDF](https://github.com/smaxer3d/LegoElements/blob/master/img/pdf.png)  
Using a scale of 75%, gave the best result in my opinion.

## Command line

```
python.exe main.py [[-Parameter] [Option]]
```
| Parameter | Function | Options            | Description                                                                                                                              |
|-----------|----------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| i         | input    | \<path><br>\<file> | - Enter a path will only get the csv-files in the directory and (re-)write the html-file<br/>- Enter a (txt-)file to create the csv-file |
| k         | key      | \<key>             | The Rebrickable API token. It can also be a file that only contains the token. If not supplied, no information is get thru this API      |

## Release notes

| Version | Date        | Description                   |
|---------|-------------|-------------------------------|
| v1.1.0  | 30 Dec 2022 | Get set image + info          |
| v1.0.0  | 29 Dec 2022 | Updated version, full release |
| v0.0.1  | 28 Dec 2022 | First commit                  |
