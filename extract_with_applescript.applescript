tell application "Keynote"
    activate
    open POSIX file "/Users/smartpo/development/projects/ניהול תרגיל מסכם/2.key"
    delay 2
    
    set slideCount to count of slides of front document
    set slideTexts to {}
    
    repeat with i from 1 to slideCount
        set slideText to ""
        try
            set slideText to text of slide i of front document
        end try
        set end of slideTexts to slideText
    end repeat
    
    return slideTexts
end tell


