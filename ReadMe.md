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

Second, an element-id, part-number, color and description doesn't help you much when you are at a shop where they sell second-hand Lego that you have to gather from large boxes of mixed pieces.  
That's where that link to an image comes in!

## Put it to use

Personally, I like to write a note.  
Especially when there is little room on the table with all the pieces spread out.  
![Note](img\note.png)

And type it to a txt-file later:  
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


## Release notes

| Version | Date        | Description  |
|---------|-------------|--------------|
| v0.0.1  | 28 Dec 2022 | First commit |
