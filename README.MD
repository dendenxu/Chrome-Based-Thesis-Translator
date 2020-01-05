# CopyTranslator

This is a small translator developed only for personal use.

## 0. Preface

### 0.0 Function Specification

- It can open a automatic software controlled Chrome window on one side of your screen, and it will try to translate things you've copied to your clipboard.
- If the stuff you copy is obviously non-text, nothing will happen.
- It won't translate things again if your previous copied text is equivalent to current one.
- It will slice large content into pieces, and translate them one by one on Google Translate, then save the translated text into a file in your current workspace: `"translated.txt"`.
- It loads the `google_translate.crx` Chrome extension to the opened Chrome session so you can use the native translation support inside the Chrome browser window.
- You can use the window like a normal Chrome window, just please don't copy things when you've navigated away from the translation tab hah.
- TODO: Support command line arguments to set translation engine.
- TODO: Support command line arguments to set default translation language source and destination.
- TODO: Modify `google_transalte.crx` so that the default pop-up option is set to **Pop-up Immediately**
  - And this requires me to learn about `JavaScript` and `TypeScript`
- TODO: Support offline translation
  - That would require a whole reconstruction of this project
  - I'm thinking about giving user options to select there favorite translation engine (online or offline)

Developed only for my own convenience, so you may feel disappointed if you want something handy. Things that feels good to me doesn't necessarily get along well with you.



### 0.1 Not Important

At the beginning of the development, I tried to use **http** request to get the translation content. And it worked, at least for a while, until Google banned my IP address after tons of translation attempt (well, not that much, it was like I used it to read merely one paper before Google banned me.)



However, if you think this software can brighten your life a little bit, feel free to download and use it.

Haven't polished the program due to poor time management, and I've left quite a lot of comments in the program. If my program seems too naïve for you, fell free to contribute or mock me :kissing_smiling_eyes:



Well, for your reference or for my own reference, I wrote this user guide.

## 1. User Guide

### 1.0 Preparations

1. Make sure **`Python3`** is correctly installed on your computer.
   - This is the base of this program, it uses python to control the chrome window.
2. Make sure **`Pywin32`** python3 library is correctly installed for your python3.
   - I used this to the the copied content from your clipboard, currently it only supports Windows
3. Make sure **`Selenium`** python3 library is correctly installed for your python3.
   - Manipulate Chrome automatically.
4. Make sure **`Chrome`** and its **Corresponding `Chrome Driver`** is correctly installed on your computer.
   - Check your Chrome driver version if things start to happen when you're using `Selenium`

### 1.1 Usage

Hereby I list common procedures for usage on Windows.

Similar procedure can also be done on MacOS or others.

1. Open a **Command Line**
2. Use **python3** to run the **translator.py** file
   - Type in command like `python translator.py` and press <kbd>ENTER</kbd>
3. Copy something and you'll get your result (the result is stored in a file called `translated.txt` if it's too large to be displayed)

Have trouble using this? Contact me on 3180105504@zju.edu.cn
