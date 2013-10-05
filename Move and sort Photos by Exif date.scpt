(*
ExifMoveAndSort by Nicolas Meier
Move and sort pictures by using Exiftool and Hazel
May 1, 2011

Last revsion: Oct 5, 2013

Pictures are moved to the Photos repository and sorted by Exif original date

ExifTool (http://www.sno.phy.queensu.ca/~phil/exiftool/)
*)

on hazelProcessFile(theFile)
	
	-- Add your logic here.
	-- 'theFile' is an alias to the file that matched.
	-- Make sure to throw errors if you do not want Hazel
	--   to consider this action to have run successfully.
	
	tell application "Finder"
		set unixPath to POSIX path of (container of (item theFile) as text)
		
		-- Force the locale to fr_FR.UTF-8 because Hazel use the wrong locale
		set LANG to "export LANG=\"fr_FR.UTF-8\""
		set LC_COLLATE to "export LC_COLLATE=\"fr_FR.UTF-8\""
		set LC_CTYPE to "export LC_CTYPE=\"fr_FR.UTF-8\""
		set LC_MESSAGES to "export LC_MESSAGES=\"fr_FR.UTF-8\""
		set LC_MONETARY to "export LC_MONETARY=\"fr_FR.UTF-8\""
		set LC_NUMERIC to "export LC_NUMERIC=\"fr_FR.UTF-8\""
		set LC_TIME to "export LC_TIME=\"fr_FR.UTF-8\""
		
		-- Guess the destination of the files
		if unixPath = "/Users/YourUser/path/to/Camera Roll/" then
			set dest to "iPhone"
		else if unixPath = "/Users/YourUser/path/to/Photon/" then
			set dest to ""
		end if
		
		-- Prepare the command
		set EXIFTOOL to Â
			"exiftool \"-Directory<DateTimeOriginal\" -d \"/path/to/target/%Y/%m - %B/" & dest Â
			& Â
			"\" " & quoted form of unixPath
		
		-- Ensure Phoenix Slides and PhotoSync are not running
		tell application "System Events" to set phoenixCount to the count of (processes whose name is "Phoenix Slides")
		tell application "System Events" to set photoSyncCount to the count of (processes whose name is "PhotoSync")
		
		if phoenixCount = 0 and photoSyncCount = 0 then
			
			-- Execute the shell script
			do shell script LANG Â
				& Â
				"; " & LC_COLLATE Â
				& Â
				"; " & LC_CTYPE Â
				& Â
				"; " & LC_MESSAGES Â
				& Â
				"; " & LC_MONETARY Â
				& Â
				"; " & LC_NUMERIC Â
				& Â
				"; " & LC_TIME Â
				& Â
				"; " & EXIFTOOL
		end if
		
	end tell
	
end hazelProcessFile