# Unbracket - A Sublime Text 3 Plugin

A plugin for [Sublime Text 3](https://www.sublimetext.com/3) that allows you to `unbracket`, i.e. remove curly brackets, square brackets, or parentheses within current selection or current line. 

Unbracket's behavior is similar to [ParentalControl](https://github.com/ilyakam/ParentalControl) but not exactly the same. Unbracket removes curly brackets, square brackets, or parentheses in a slightly different way. See the GIF below to see this in effect.

![Demo GIF](https://user-images.githubusercontent.com/7110058/29059559-fd25a4ea-7bca-11e7-9ccb-19d40377b917.gif)


## Features
1. Unbracket attempts to be safe, which means, if no matching brackets are found, Unbracket does nothing.
2. Unbracket recognizes `"` and `'` as quote characters and works correctly even when the expression contains balanced, possibly nested quotes. For unbalanced, nested quotes, see Known Limitations section below.
3. Unbracket was designed to work with R and Python code but may work with other programming languages too. 

## Installation
Unbracket is not yet available on Sublime Package Manager. You can simply clone the repository inside `Packages` folder.

```
# MacOS
cd ~/Library/Application Support/Sublime\ Text\ 3/Packages
git clone git@github.com:ankur-gupta/Unbracket.git

# Linux
cd ~/.config/sublime-text-3/Packages
git clone git@github.com:ankur-gupta/Unbracket.git
```

## Usage 
Unbracket comes with these default key bindings out of the box but you can change them.

**MacOS**: `Command+Shift+[` to unbracket

**Linux**: `Control+Shift+[` to unbracket


## Known Limitations
1. Unbracket cannot handle multiple lines. If your expression spans multiple lines, unbracket will likely not do anything.
2. Unbracket cannot handle nested quotes. As an example, unbracket cannot handle `"'"`. But, unbracket should work fine on balanced nested quotes like `"''"`.



