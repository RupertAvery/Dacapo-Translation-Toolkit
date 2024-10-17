# Da Capo Script Translation Tool

〜ダ・カーポ〜 (Da Capo) is a Japanese adult visual novel developed by Circus.

This tool is a set of python scripts that allows you to:

* Dump the `.OBJ` files from `script.bin`
* Decode `.OBJ` files int `.TXT` files, which contain the script
* Encode `.TXT` files back into `.OBJ` files
* Join `.OBJ` files back into one `script.bin`

This tool is targeted for the PSP version, but it might work on other platform versions if the byte script is the same.

# Setup

* Install Python 3.10
* Extract `PSP_GAME\USRDIR\data\script.bin` from the DaCapo ISO using 7zip or any tool that can extract files from an ISO
* Copy `script.bin` to this folder 

# Usage 

## Unpacking `script.bin`

The `script.bin` file is a packed file containing several `.obj` files containing the byte scripts, and pointers in the header to locate the `.obj` files in the packed file. 

First we will unpack the `.obj` files. To unpack the file, open a command terminal and run the command:

```
unpack script.bin
```

or simply

```
unpack
```

A folder named `obj` will be created, containing 1406 files named `block(number).obj` and a file named `script.manifest`

## Decoding an `.obj` file

The `.obj` files contain byte script and Shift-JIS encoded text. To decode them into an editable script file, run the following command:

```
decode block1
```

Or, to decode all the files:

```
decode all
```

## Encoding a `.txt` file

To encode a `.txt` file back into an `.obj` file, run the following command.

NOTE: This will overwrite the `.obj` file without confirmation!

```
encode block1
```

Or, to encode all the files:

```
encode all
```

## Packing `script.bin`

When you want to rebuild `script.bin` for testing, run the following command.

```
pack build/script.bin
```

A folder named `build` will be created and the compiled `script.bin` containing your changes will be placed there.


# Scripts

Scripts are decoded text representations of the byte script, containing tokens and text that will be translated to byte commands when compiled into an `.obj` file.

Not all of the commands are decoded into tokens, and some of the tokens purposes are only guessed at. Changing anything other than text is currently not supported, and will likely crash the game.

**NOTE:** Scripts must be saved using UTF-8 encoding

## Tokens

`[BYTES] DE AD BE FF ...` 

* Followed by any number of bytes, separated by spaces
* Outputs raw bytes to the OBJ file

`[VOICE] AA BB CC` 

* Followed by 3 bytes, separated by spaces
* Plays a voice clip

`[BGM]`

* Followed by 3 bytes, separated by spaces
* Sets the background music

`[SFX]`

* Followed by 3 bytes, separated by spaces
* Plays a sound effect(?)

`[SET_BACKGROUND] AA BB CC DD EE FF GG HH`

* Followed by 7 bytes, separated by spaces
* Seems to set the background, but may depend on other state

`[REMOVE_ACTOR] AA`

* Followed by 1 byte
* Seems to remove an actor from the stage
* AA determines which actor slot to remove from?

`[SHOW_ACTOR] AA BB CC DD EE FF GG HH II JJ`

* Followed by 9 bytes
* Seems to add an actor to the stage
* AA determines which actor slot to add the character to?
* BB determines which character to load into the slot?

`[TEXT] Some Text to Display`

* Followed by text
* Displays text in the dialog box
* Multiple lines are allowed. The next line should just continue with the text (no starting token)
* The last line must be an empty line
* There may be a limit of 3 lines
* There may be a limit to the number of characters per line
* See [Text](#text)
* Furigana is supported. See [Furigana](#furigana)

`[CLEAR_NAME]`

* Clears the name above the dialog box

`[SET_NAME] Some name`

* Followed by text
* Sets the name above the dialog box to "Some name"
* There may be a limit to the number of characters in the name

`[SCENE]`

* Occurs before any tokens that modify the scene

`[JUNICHI]`

* Sets the name above the dialog box to the main character, Junichi

`[START-CHOICE]`

* Occurs at the start of a choice set
* Displays a set of choices for the player to interact with

`[CHOICE] Choice text`

* Displays the Choice text as a choice in a choice set

`[CHOICE-OFFSET] Labelname`

* Occurs before a `[CHOICE]` token
* Causes the script to jump to the Label given by `Labelname`

`[END-CHOICE]`

* Occurs at the end of a choice set

`[LABEL] Labelname`

* Defines a Label named `Labelname`.  Used to calculate the offset for [CHOICE-OFFSET] jump.
* Does not output any bytecode


## Text

While the scripting engine seems to support Latin characters, Arabic numbers, and punctuation symbols, the full extent of supported characters is unknown, so support for diacritics is unknown.

The decoded `.txt` script is saved and read as UTF-8, while the `.obj` file it is compiled to uses Shift-JIS encoding.

## Furigana 

The scripting engine has a special way to encode furigana (the small kana above kanji). To do this, write the kana followed by `\xEF\xBC\x8F` (not a forward slash!) then the kanji, wrapped in curly braces `{ }`

e.g.

```
{しんしん／深々｝
```

There should probably be two kana per kanji

