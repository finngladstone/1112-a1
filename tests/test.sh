today=`date '+%b %d  %Y'`
name=`id -u -n`
group=`id -gn`

# resets directory 
PRESERVE="test.sh"|"pcontrol.py"

rm -rf !$PRESERVE

# test program correctly handles missing file list 

touch exp_output.txt 
echo "" > exp_output.txt

python3 pcontrol.py

# start by testing permissions flip: examine chmod values as well as output!

touch test_1.ext 
touch test_2.ext 

echo "initialised test_1 and test_2"

chmod 463 test_1.ext 
chmod 173 test_2.ext 

echo "test_1 set to group read/write @ 463"
echo "test_2 set to group r/w/exec @ 173"

test_1_size=`du -k "test_1.ext" | cut -f1`
test_2_size=`du -k "test_2.ext" | cut -f1`



touch filelist.txt 

echo "test_1.ext
test_2.ext" > filelist.txt

touch exp_output.txt 
echo "test_1.ext Group Readable: True, Group Executable: False Size: $test_1_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" > exp_output.txt
echo "test_2.ext Group Readable: True, Group Executable: True Size: $test_2_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" >> exp_output.txt

python3 pcontrol.py

diff exp_output.txt output.txt # tests if output is correctly formatted! 

# https://stackoverflow.com/questions/26949492/how-to-check-chmod-using-bash-numeric

test_1_perms=`stat -c "%a" test_1.ext`
test_2_perms=`stat -c "%a" test_2.ext`

echo "chmod for test_1: $test_1_perms"
echo "chmod for test_2: $test_2_perms"

# test if program recognises files in subdirectories 
mkdir -p moretests
touch moretests/test_3.ext 

cd moretests

chmod 364 test_3.ext 

test_3_size=`du -k "test_3.ext" | cut -f1`

cd ..

echo "test_3.ext" >> filelist.txt 

# also test for permissions flip formatted correctly in output file for test_1 and test_2 

echo "test_1.ext Group Readable: True, Group Executable: True Size: $test_1_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" > exp_output.txt
echo "test_2.ext Group Readable: True, Group Executable: False Size: $test_2_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" >> exp_output.txt
echo "test_3.ext Group Readable: True, Group Executable: False Size: $test_3_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" >> exp_output.txt

python3 pcontrol.py 

diff exp_output.txt output.txt 

test_3_perms=`stat -c "%a" moretests/test_3.ext`
echo $test_3_perms  

