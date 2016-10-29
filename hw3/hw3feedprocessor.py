
### you will need this function later in the homework
def stripWordPunctuation(word):
    return word.strip(".,()<>\"\\'~?!;*:[]-+/&")

print "== part 3 =="
### part 3: fieldType() function
# In hw3feed.txt, note that there are both posts and comments in this feed. There are also posters.
# These lines each start with post:, comment:, and from: respectively.
# You are probably thinking "it would be really helpful if we had a function that I could
# use to figure out which type of content a line contains."
#
# The good news is that now you will write that function. 
#
# We have included some starter code to define a function fieldType(). This function should take a line as
# parameter and return the field type (either post, comment, or from).

def fieldType(line):
    for i in line:
        if i[0] == "p":
            return "post"
        elif i[0] == "c":
            return "comment"
        else:
            return "from"

# You can uncomment and test your function with these lines
print fieldType("from: Sean")
print fieldType("post: Hi everyone")
print fieldType("comment: Thanks!")

print "== part 4 =="
# Find out and print how many posts there are
# as well as how many comments there are
# 
# Print them as:
# Total posts: <number>
# Total comments: <number>
#

posts = 0
comments = 0

fname = "hw3feed.txt"
f = open(fname,'r')

for i in f:
    if i[0] == "p":
        posts += 1
    elif i[0] == "c":
        comments += 1


print "Total posts: %d"%posts
print "Total comments: %d"%comments

print "== part 5 =="
### part 5: printing users

# Your job is to extract the names form the post: lines and print them out,
# exactly as it is shown in the screenshot in the PDF file. Hint: if you 
# want to remove "from:" you can use string slicing operations or the replace method.

# You may use the fieldType() function but you do not have to. You may also define
# another function, such as fieldContents(), to help you but that optional. 

# Duplicate names are expected for this part!

fname = "hw3feed.txt"
f = open(fname,'r')
for i in f:
    if i[0] == "f":
        print i[5:].strip('\n')


print "== part 6 =="
### part 6: counting poster contribution frequency
# See the instructions in the PDF file. They are easier to follow with
# formatting

pc_count = {}
f = open(fname,'r')

# read in and count the total number of posts and comments for each user

for i in f:
    if i[0] == "f":
        name = i[5:]
        if name in pc_count:
            pc_count[name] += 1
        else:
            pc_count[name] = 1

# print the number of times each user posted

for k in pc_count.keys():
    print k.strip('\n') + ": " + str(pc_count[k])


# part 6 - Just for fun: how many unique posters were there?
# (note this question is optional - but it's one line of code)

#print len(pc_count.keys())

print "== part 7 =="
### part 7: counting word frequency
# This is similar to post count in part 6 and you might
# even re-use some of your code. Count the number of
# times each word appears in all posts, but *not* comments
#
# use the stripWordPunctuation() function to get rid of punctuation.
# note that it is not perfect so some extra punctuation may remain.
#
# you should also convert all words to lowercase when counting.
# I.e., "the" and "The" should be the same word

postWordCount = {}
f = open(fname,'r')

# read in and count of times each word appeared

for i in f:
    if i[0] == "p":
        words = i.split()
        for j in words:
            word = stripWordPunctuation(j.lower())
            if word in postWordCount:
                postWordCount[word] += 1
            else:
                postWordCount[word] = 1

# print the number of times each word appeared

for k in postWordCount.keys():
    print k + ": " + str(postWordCount[k])


print "== part 8 =="
### part 8: counting word frequency in comments and posts
# for this part, write a function, wordFreq() that will return
# the word frequency in either posts or comments as a dictionary

# This function must must take a file name and the field type
# (either post or comment) as parameters

# For example, if I want to get a dictionary of word counts in
# the posts in hw3feed.txt, I should be able to call:
# wordFreq('hw3feed.txt','post')

# You can use your code from part 7 as a starting point, or
# if you wrote part 7 using a function, you may simply edit it
# to meet the requirements for this part.

# uncomment and begin editing from the next line:
def wordFreq(fileName, fieldType):
    f = open(fileName, 'r')
    if fieldType == "post":
        posts = {}
        for i in f:
            if i[0] == "p":
                words = i.split()
                for j in words:
                    word = stripWordPunctuation(j.lower())
                    if word in posts:
                        posts[word] += 1
                    else:
                        posts[word] = 1
        return posts
    else:
        comments = {}
        for i in f:
            if i[0] == "c":
                words = i.split()
                for j in words:
                    word = stripWordPunctuation(j.lower())
                    if word in comments:
                        comments[word] += 1
                    else:
                        comments[word] = 1
        return comments
        

# to test ,you can uncomment and run these  lines:
if wordFreq(fname,'post')["anyone"] == 9 and wordFreq(fname,'post')["eclipse"] == 5:
    print "Looks like wordFreq() works fine for posts"
else:
    print "We got some errors with wordFreq() for posts."
  
if wordFreq(fname,'comment')["file"] == 24 and wordFreq(fname,'comment')["if"] == 39:
    print "Looks like wordFreq() works fine for comments"
else:
    print "We got some errors with wordFreq() for comments."

