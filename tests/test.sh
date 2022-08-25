shopt -s extglob # allows us to reset the directory in one line 

today=`date '+%b %d  %Y'`
name=`id -u -n`
group=`id -gn`

# resets directory - https://superuser.com/questions/529854/how-to-delete-all-files-in-a-directory-except-some
rm -rf !("test.sh"|"pcontrol.py")

# test program correctly handles missing file list 

touch exp_output.txt 
echo "filelist.txt can not be found" > exp_output.txt

check_1() {
    if diff exp_output.txt output.txt; then
        check_1_result='PASSED'
    else 
        check_1_result='FAILED'
    fi
}

echo "--- First execution cycle ---"
python3 pcontrol.py # should run, create output.txt, and report missing filelist.txt
check_1
echo "Testing program handles missing filelist.txt... $check_1_result" 

# create filelist but add invalid path 
touch filelist.txt 
mkdir test_dir
echo "test_1.ext" > filelist.txt 
echo "test_dir" >> filelist.txt
echo "test_1.ext can not be found" > exp_output.txt
echo "test_dir: Invalid type, Please enter a file" >> exp_output.txt

echo "--- Second execution cycle ---"
python3 pcontrol.py

check_1
echo "Testing program handles invalid file name and broken directory... $check_1_result"

# start by testing permissions flip: examine chmod values as well as output!

touch test_1.ext 
touch test_2.ext 

#initialised test_1 and test_2

chmod 766 test_1.ext 
chmod 774 test_2.ext 

# test_1 set to group read/write @ 766
# test_2 set to group r/w/exec @ 774

test_1_size=`du -k "test_1.ext" | cut -f1`
test_2_size=`du -k "test_2.ext" | cut -f1`

# create + modify filelist to include the two test files 
echo "test_1.ext" > filelist.txt
echo "test_2.ext" >> filelist.txt

touch exp_output.txt 
echo "test_1.ext Group Readable: True, Group Executable: False Size: $test_1_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" > exp_output.txt
echo "test_2.ext Group Readable: True, Group Executable: True Size: $test_2_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" >> exp_output.txt

echo "--- Third execution cycle ---"
python3 pcontrol.py

check_1 # run diff test again

echo "Testing output file formatting, correct reading of permissions... $check_1_result"

# https://stackoverflow.com/questions/26949492/how-to-check-chmod-using-bash-numeric


check_2() { # checks that permissions bits have been correctly flipped for test_1 and test_2
    test_1_perms=`stat -c "%a" test_1.ext`
    test_2_perms=`stat -c "%a" test_2.ext`
    if [[ test_1_perms -eq 776 ]]; then
        if [[ test_2_perms -eq 764 ]]; then 
            check_2_result='PASSED'
        else 
            check_2_result='FAILED'
        fi
    else 
        check_2_result='FAILED'
    fi
}

check_2

echo "Testing that permissions bits are correctly modified in chmod... $check_2_result"

mkdir -p moretests
touch moretests/test_3.ext 

cd moretests

chmod 761 test_3.ext 

test_3_size=`du -k "test_3.ext" | cut -f1`

cd ..

echo "test_3.ext" >> filelist.txt 

# also test for permissions flip formatted correctly in output file for test_1 and test_2 

echo "test_1.ext Group Readable: True, Group Executable: True Size: $test_1_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" > exp_output.txt
echo "test_2.ext Group Readable: True, Group Executable: False Size: $test_2_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" >> exp_output.txt
echo "test_3.ext Group Readable: True, Group Executable: False Size: $test_3_size, Owner: $name, Group: $group, last modified date: $today, last access date: $today" >> exp_output.txt

echo "--- Fourth Execution Cycle ---"
python3 pcontrol.py 

check_1 # run diff test again

echo "Testing for file in subdirectory + permissions flip in output.txt... $check_1_result"

check_3() {
    test_3_perms=`stat -c "%a" moretests/test_3.ext`
    if [[ test_3_perms -eq 771 ]]; then
        check_3_result='PASSED'
    else 
        check_3_result='FAILED'
    fi
} 

check_3
echo "Testing that file in subdirectory was successfully flipped in chmod... $check_3_result"