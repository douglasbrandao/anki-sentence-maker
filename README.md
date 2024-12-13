# Anki Sentence Maker

**Anki Sentence Maker** is a personal project that helped me increase my vocabulary in english and it stemmed in how I conduct my study:
- Listen to a new word
- Look it up in an online dictionary
- Save in a csv file
- Import on my Anki

I know that AI could do it more easily, but I'm an old fashioned guy 🤠

## Requirements

* [Python 3](https://www.python.org/downloads/)
* [pip](https://pypi.org/project/pip/)

## Getting started

Go to the directory where requirements.txt is located and run 

```
pip install -r requirements.txt
```

After install all the packages, you can run the main.py file passing the arguments

```
python3 main.py desecrate meaning
```

In case you are searching expressions separated by spaces, wrap it up with quotation marks
> Example: a means to an end

```
python3 main.py desecrate "a means to and end" meaning
```

The script will try to find these words, and it will save into the root folder following the format below

```
sentences-25-04-2020.csv
```

And that's it. You can import the .csv file in your Anki.

## How it works

* User provide a list of words
* The script look it up in several online dictionaries
* The script create a .csv file with rows following the format below

## Card format

|Sentence (Front card) |Information (Back card)|
|:-------------:|:-------------:|
|He played with the band at a recent gig.| gig /ɡɪɡ/ (a performance by musicians playing popular music or jazz in front of an audience; a similar performance by a comedian)|

> This way we have the information about the word such as a short definition and its phonetic notation.

## Dictionaries implemented

* Cambridge Dictionary
* Oxford Dictionary

## To the future

* Collins Dictionary, MacMillan, etc.

## Author

[Douglas Brandão](https://github.com/douglasbrandao)
