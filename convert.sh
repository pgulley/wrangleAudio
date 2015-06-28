for file in /Loops/*
do
	echo $file
	afconvert -v -f WAVE -d LEI16 "$file"
done	
