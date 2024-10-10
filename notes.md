NOTE:

Script is loaded into 0x09ECE800

#

22 01 22 00 01 00 00 22 00 2F 04 2F 02 

39 00 3F 00 
<Fade to white>
[CHANGE_BG] 5F 05 30 00 35 02 5F 06 
[CHANGE_BG] 5F 05 30 00 35 03 5F 06 


BLOCK 4
====================================================
20 00 20 01 5D 00 20 01 5E 00 20 01 5F 00 20 01 E1 01 20 01 8E 02 20 01 8F 02 20 0F 23 00 1F 00 00 00 00 22 01 30 00 00 00 00 04 00 22 00 25 00 22 01 22 00 01 00 00 04 00 22 00 18 00 22 01 2E 00 00 00 00 04 00 22 00 0B 00 23 00 1F 00 00 01 00 22 00 D7 12 23 00 1F 00 00 00 00 23 00 25 00 00 02 00 23 00 20 00 00 17 00 23 00 27 00 00 05 00 
[CHANGE_BG] 5F 05 30 00 35 03 5F 06 
[TEXT] まぶたに染み込む朝日に視覚神経を刺激され、
俺は｛かくせい／覚醒｝の時を迎えた。

14 00 01 

# Girl in bed, light music

[CHANGE_BG] 5F 05 
3C 0D 35 01 D6 04 00 00 00 00 00 
5F 06 
45 00 

# Girl in bed, eyes half closed

[CHANGE_BG] 5F 05 
3C 0D 35 01 D7 04 00 00 00 00 00 
5F 06 
45 00 

# Stop music???
[PLAY_CLIP] 22 00 00

# Shake screen

[CHANGE_BG] 35 0C 

# Fade to white

[CHANGE_BG] 5F 05 30 00 35 03 5F 06


08 00 01 

# Bedroom #1, Music #3, Girl in uniform with yellow ribbons, face #1 (smiling)

43 04 5F 05 3C 0D 35 01 FF 03 00 00 00 00 00 5F 06 
45 01 13 00 
3C 00 00 
3C 0F 
3C 01 00 A9 00 00 64 00 00 00 00 3C 0F 

# Girl in uniform with yellow ribbons, face #2 (concerned?)

[CHANGE_BG] 
3C 01 00 AE 00 00 64 00 00 00 00 3C 0F

# Fade to black

[CHANGE_BG] 
5F 05 
30 00 
35 02 
5F 06 
3C 00 00 
3C 0F 

# Bedroom #1, no characters

[CHANGE_BG] 
5F 05 
3C 0D 35 01 FF 03 00 00 00 00 00 
5F 06 

# Girl in uniform with yellow ribbons, face #3 (eyes closed, sad)

[CHANGE_BG] 
3C 00 00 
3C 0F 
3C 01 00 B3 00 00 64 00 00 00 00 
3C 0F

# Girl in uniform with yellow ribbons, face #4 (eyes closed, mouth open, happy?)

[CHANGE_BG] 
3C 01 00 AA 00 00 64 00 00 00 00 
3C 0F

# Remove character

[CHANGE_BG] 
3C 00 00 
3C 0F

# Girl in uniform with yellow ribbons, face #2 (concerned?)

[CHANGE_BG] 
3C 00 00 
3C 0F 
3C 01 00 AE 00 00 64 00 00 00 00 
3C 0F

# Girl in uniform with yellow ribbons, face #2 (alarmed?)

[CHANGE_BG] 
3C 01 00 B0 00 00 64 00 00 00 00 
3C 0F 

# Play music #???

14 00 01 

# Stop music? Thud?

1B 00 00 

# Girl in uniform with yellow ribbons, face #5 (hand on face?)

[CHANGE_BG] 3C 01 00 B9 00 00 64 00 00 00 00 3C 0F 

# Play happy music?

08 00 01

# Girl in uniform with yellow ribbons, face #6 (angry/annoyed)

[CHANGE_BG] 3C 01 00 B6 00 00 64 00 00 00 00 3C 0F 

# Choice???


3C 0E 3C 0F 

46 00 

46 02 3A 00 [CHOICE] ○まぁ、起きたほうがいいな - go to block 6

46 02 48 00 [CHOICE] ○後５分…… - go to block 2

46 0F 01 01 00 0A 

22 01 
22 00 01 00 00 
22 00 2F 04 2F 02 


# Park scene (cheey blossoms)? Playing twinkle twinkle sound

2F 03 30 00 01 
[CHANGE_BG] 
5F 05 
3C 0D 35 01 F5 03 00 00 00 00 00 
5F 06 
45 01 12 00 39 01 02 02 3F 01 02 02 
43 05 

# Green haired girl with lollipop, eyes closed

[CHANGE_BG] 
3C 00 00 
3C 0F 
3C 01 00 EE 00 00 64 00 00 00 00 
3C 02 00 0C 00 00 64 00 00 00 00 
3C 0F 
43 05 

# Clear character and then ...?

[CHANGE_BG] 
3C 00 00 
3C 0F 
3C 03 00 
3C 0F 
43 05 

# Classroom #1 with short green haired girl, chill music

2F 02 39 00 3F 00 
[CHANGE_BG] 5F 05 30 00 35 02 5F 06 
24 00 01 00 
[CHANGE_BG] 5F 05 30 00 35 02 5F 06 
24 00 B6 03 
2F 06 0A 00 01 
[CHANGE_BG] 5F 05 
3C 0D 35 01 DA 03 00 00 00 00 00 
5F 06 
45 01 08 00 
43 05 

# Display 2 characters side by side
# Sakura on left, blue haired guy on right

[CHANGE_BG] 
3C 00 01 
3C 0F 
3C 01 00 AA 00 00 64 88 FF 00 00 
3C 01 01 FE 00 00 64 78 00 00 00 
3C 0F 43 05 
[PLAY_CLIP] 08 00 0E


# Doesn't seem to change the scene
[CHANGE_BG] 3C 01 01 FC 00 00 64 78 00 00 00 3C 0F 43 05 
[CHANGE_BG] 3C 01 00 AB 00 00 64 88 FF 00 00 3C 0F 43 05 

# Remove character in slot 1

[CHANGE_BG] 
3C 00 00 
3C 0F 
43 05 

# fade to black?

[CHANGE_BG] 5F 05 30 00 35 02 5F 06 24 00 01 00 
[CHANGE_BG] 5F 05 30 00 35 02 5F 06 43 05 


[CHANGE_BG] 
5F 05 
3C 0D 35 01 DA 03 00 00 00 00 00 
5F 06 
3C 00 00 
3C 0F 
3C 01 00 FE 00 00 64 00 00 00 00 
3C 0F 
43 05 

22 01 30 00 00 00 00 04 00 
22 00 25 00 
22 01 22 00 01 00 00 04 00 
22 00 18 00 
22 01 2E 00 00 00 00 04 00 
22 00 0B 00 

22 01 22 00 01 00 00 22 00 
2F 04 
2F 02 
22 01 30 00 00 00 00 04 00 

22 01 22 00 01 00 00 22 00 
2F 04 
2F 02 
01 01 00 0A 
22 01 22 00 01 00 00 22 00 
2F 04 
2F 02 
22 00 30 FE 01 01 00 0A 00 






43 04 
5F 05 3C 0D 
35 01 FF 03 00 00 00 00 00
5F 06 45 01 13 00 
3C 00 00
3C 0F
3C 01 00 A9 00 00 64 00 00 00 00
3C 0F
2F 00 23 00 00