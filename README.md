# bookmarks2org
Converts firefox bookmarks to org-mode format, modified from: http://rexim.me/firefox-bookmarks-to-org-mode.html

# Updates 2018, Fabio Rinaldi
- changed the structure of the recursive loop to make it more easily
  modifiable
- added a default container title, which will be used if none is
  provided in the json file
- the script now accepts command-line arguments. If none are provided,
  it converts the entire json file. If there are arguments, they will
  be treated as container titles to be matched in the json file. Only
  containers which have an exact match will be converted, all the rest
  discarded. 
